#!/usr/bin/env python3
"""RouteMind over MCP — so any MCP-capable agent can read this ontology.

    knowledge-mcp --api http://localhost:8080/api/knowledge

Four tools (operator, 2026-10-07: "Simple is best"):

    knowledge_table(path?, why)   a routing table — with no path, hop 0, where every walk starts
    knowledge_read(path, why)     one document
    knowledge_place(op)           put a new document where the table says it goes, by walking it
    knowledge_circuit(op)         read another RouteMind for the length of this connection

Every walk starts at hop 0: below it, a table or a document is refused until hop 0 has been opened in
this session, and every step carries a one-line reason that the footprint records
(docs/FOOTPRINT.md). `knowledge_overlay` and `knowledge_write` exist and are off unless
KNOWLEDGE_TOOLS_EXTRA turns them on.

An agent never composes an address. Every row a table prints carries the exact `path` that fetches
it, which is why the structure can move without breaking a caller. Addresses assembled by the caller
broke once already, silently, when documents moved one level down.

Stdlib only, and one file, for the same reason the ontology service is: it has to be trivially
runnable by someone who has not set this project up.

What an agent is handed here is the same shape the map previews and the same shape a web console
gets. There is one advertisement, and every engine reads it.
"""
from __future__ import annotations

import argparse, time
import datetime as _dt
import ipaddress
import json
import socket
import re
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

PROTOCOL_FALLBACK = "2024-11-05"
# What each row is, which is the same thing as which tool answers it. `empty` is the third state: an
# entity nobody has written into yet — neither a table nor a document. Calling it a table sends an
# agent a hop to find nothing, which is the mistake this column exists to prevent.
KIND = {"table": "table", "file": "file", "empty": "empty", "outside": "outside"}


# ── the API ───────────────────────────────────────────────────────────────────

class Api:
    def __init__(self, base: str, actor: str, timeout: float = 30.0):
        self.base = base.rstrip("/")
        self.actor = actor
        self.timeout = timeout

    def _get(self, path: str, accept: str, method: str = "GET", body: dict | None = None):
        # `base` is the v1 root — the web proxy at /api/knowledge, or an ontology at .../v1 — and
        # every address in this system is written as the tables print it, beginning `/v1/`. Stripping
        # that prefix happens here and nowhere else: it used to happen in each caller, and the one
        # address this module composes rather than reads then came out without it.
        url = self.base + (path[3:] if path.startswith("/v1/") else path)
        headers = {
            "Accept": accept,
            # Percent-encoded: HTTP headers are latin-1, and a name that is not ASCII either arrives
            # mangled or cannot be sent at all.
            "X-Knowledge-Actor": urllib.parse.quote(self.actor[:64], safe=""),
            # The same name, for an ontology reached directly rather than through the web proxy.
            "X-Actor": urllib.parse.quote(self.actor[:64], safe=""),
        }
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, method=method, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:400]
            detail = ""
            try: detail = (json.loads(body).get("detail") or json.loads(body).get("error") or "")
            except Exception: detail = body
            raise ApiError(f"HTTP {e.code} from {path}" + (f" — {detail}" if detail else ""), e.code)
        except (urllib.error.URLError, TimeoutError) as e:
            raise ApiError(f"RouteMind is unreachable at {self.base} ({e})")

    def json(self, path: str) -> dict:
        raw = self._get(path, "application/json")
        try: return json.loads(raw)
        except Exception: raise ApiError(f"{path} did not return JSON")

    def text(self, path: str) -> str:
        return self._get(path, "text/markdown, text/plain, */*")

    def send(self, method: str, path: str, body: dict) -> dict:
        raw = self._get(path, "application/json", method, body)
        try: return json.loads(raw)
        except Exception: raise ApiError(f"{path} did not return JSON")


class ApiError(Exception):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


# ── the tables an agent is handed ─────────────────────────────────────────────
#
# Three columns and a footer, identical at every hop, because a model that has learned to read one
# table has then learned to read all of them. `KIND` names the tool to call, so choosing a row and
# choosing a tool are one decision rather than two.

def _clip(text: str, limit: int) -> str:
    s = " ".join(str(text or "").replace("*", "").replace("`", "").split())
    return s if len(s) <= limit else s[: limit - 1] + "…"


def _since(iso: str | None) -> str:
    """An ISO stamp as an age: `3y`, `4mo`, `12d`, `today`. Empty when it is not known.

    Relative, because the question a reader is answering is "is this old", and no model reasons about
    that from a date without also knowing today's. Coarse on purpose — a row is being chosen, not
    audited, and `2y` says everything `2y 3mo 11d` would.
    """
    if not iso: return ""
    try:
        t = _dt.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError:
        return ""
    days = (_dt.datetime.now(_dt.timezone.utc) - t).days
    if days < 1: return "today"
    if days < 60: return f"{days}d"
    if days < 730: return f"{days // 30}mo"
    return f"{days // 365}y"


def _age(row: dict) -> str:
    """`route / document` — how long this path has been here, and when what it points at last moved.

    Two numbers because one cannot say both, and the pair is the whole signal: `3y / 2d` is a settled
    path over material somebody rewrote last week, and `3y / 3y` is the row worth asking about. A
    single "age" would have collapsed those two into the same warning.

    Blank when the history cannot be read. Blank means *not known* and never *new* — a document whose
    age is unavailable must not be the one that looks freshest on the page.
    """
    a, b = _since(row.get("route_since")), _since(row.get("changed"))
    # `—`, not blank. A blank cell beside columns of `18d / 18d` reads as *no age* — as if this row
    # were somehow outside time — when what it means is that the age is not ours to know. The row
    # most often in that state is one that came across a link, where the history belongs to the
    # backbone that owns it and has not crossed.
    if not a and not b: return "—"
    return f"{a or '?'} / {b or '?'}"


# What a reader is choosing on when two rows cover one subject, in the order they should be preferred.
# The words are plain rather than `own`/`grafted`/`peer`: a person reading a table is deciding whose
# answer to quote, and "ours" says that where "own" reads like a flag.
WHOSE = {"ours": "ours", "copied": "copied", "theirs": "theirs"}


def _table(rows: list[dict], title: str, lead: str, foot_absence: str | None) -> str:
    if not rows:
        # An empty table still has to say what its emptiness means. Without the footer, "(nothing
        # here)" is the strongest claim on the page and the only one with no scope attached — an
        # agent can read it as "this does not exist" while six other areas go unlooked-at.
        tail = f"\n\n{foot_absence}\n" if foot_absence else "\n"
        return f"{title}\n{lead}\n\n  (nothing here){tail}"
    addr_w = max(len(r["address"]) for r in rows)
    kind_w = max(len(r["kind"]) for r in rows)
    ages = {id(r): (r.get("age") or "") for r in rows}
    age_w = max((len(v) for v in ages.values()), default=0)
    whose = {id(r): WHOSE.get(r.get("whose") or "", "") for r in rows}
    # Only where it says something. A table whose rows are all `ours` is every table on a backbone
    # that has grafted nothing and linked to nobody, and a column of one repeated word there is ink
    # that teaches a reader to skip the place the answer will eventually appear.
    show_whose = len({v for v in whose.values() if v}) > 1
    whose_w = max((len(v) for v in whose.values()), default=0) if show_whose else 0
    out = [title, lead, ""]
    head = f"  {'KIND'.ljust(kind_w)}  {'ADDRESS'.ljust(addr_w)}  "
    if age_w: head += f"{'AGE'.ljust(age_w)}  "
    if whose_w: head += f"{'FROM'.ljust(whose_w)}  "
    out.append(head + "WHY YOU WOULD PICK THIS ROW")
    for r in rows:
        line = f"  {r['kind'].ljust(kind_w)}  {r['address'].ljust(addr_w)}  "
        if age_w: line += f"{ages[id(r)].ljust(age_w)}  "
        if whose_w: line += f"{whose[id(r)].ljust(whose_w)}  "
        out.append(line + _clip(r["why"], 100))
    out.append("")
    if whose_w:
        out.append("  FROM says whose answer a row is, and they are not interchangeable:")
        out.append("    ours    — written here, and maintained here.")
        out.append("    copied  — grafted from another backbone. A snapshot of what they had, which")
        out.append("              nobody here has been keeping up to date since.")
        out.append("    theirs  — read across a link, right now. Theirs to change, and about their")
        out.append("              organisation rather than yours.")
        out.append("  When two rows cover the same subject, prefer `ours`. Quoting one of the others")
        out.append("  as this organisation's answer is the mistake this column exists to prevent —")
        out.append("  say whose it is.")
    if age_w:
        # Said once, under the table, because a column of `3y / 2d` with nothing explaining it is
        # read as one number twice. The second half is the one that answers "should I look for
        # something newer"; the first says whether this path has been settled or was just laid down.
        out.append("  AGE is how long this route has been here / when its document last changed.")
        out.append("  An old route over a recently changed document is current. An old route over a")
        out.append("  document that has not moved is the one to ask about before quoting it.")
        if any((r.get("age") or "") in ("—", "") or "?" in (r.get("age") or "") for r in rows):
            out.append("  `—` is not known here — usually a row from across a link, whose history stays")
            out.append("  with the backbone that owns it. Not known is not the same as new.")
    out.append("  table → knowledge_table({ path })    ·    file → knowledge_read({ path })")
    if any(r["kind"] == KIND["empty"] for r in rows):
        out.append("  empty → nobody has written it yet. Do not fetch it; say so if it is what was asked for.")
    out.append("  Use the address exactly as printed above. Never build one.")
    if foot_absence:
        out.append("")
        out.append(foot_absence)
    return "\n".join(out) + "\n"


def hop0(api: Api) -> str:
    """The list every run reads before it chooses anything.

    This is the one table that may state absence, and it says so out loud. It is true of the whole
    list and of nothing smaller: an area's own table is a list of what that area holds, not a claim
    about the world, and a model told otherwise will answer "there is no such thing" from inside one
    area.
    """
    d = api.json("/v1/regions")
    rows = [{"kind": KIND["table"], "address": r.get("fetch") or f"/v1/regions/{r.get('source')}",
             "why": r.get("use_when") or r.get("description") or r.get("title") or "",
             "age": _age(r), "whose": r.get("whose")}
            for r in (d.get("regions") or [])]
    # The API supplies this sentence when it is not the plain one — when this backbone is linked to
    # others, and above all when a link is down. Whether the list is still the whole world is not
    # something this side can know: only the thing that just tried to read every peer knows, and
    # printing the confident sentence over an incomplete list is the one failure this table must
    # never have. See _absence in ontology/service/server.py.
    absence = d.get("absence") or (
        "Nothing outside this list exists in RouteMind. This list is the grounds on which you may say\n"
        "something is absent — no smaller table is.")
    return _table(
        rows,
        "ROUTEMIND — the areas of this domain",
        "Pick the row whose condition matches the question, then fetch it. One step, then read.",
        absence,
    )


def area(api: Api, path: str) -> str:
    d = api.json(path)
    rows = []
    for e in (d.get("entries") or []):
        kind = {"data": KIND["file"], "empty": KIND["empty"]}.get(e.get("type"), KIND["table"])
        why = f"{e.get('name') or e.get('id')} — {e.get('one_liner') or ''}"
        if kind == KIND["empty"]: why += "  (nothing written here yet)"
        rows.append({"kind": kind, "address": e.get("fetch") or "", "why": why, "age": _age(e), "whose": e.get("whose")})
    head = f"{d.get('key') or path} — {d.get('advertises') or ''}".strip(" —")
    lead = (f"When to be here: {d['use_when']}" if d.get("use_when") else "") or "What this area holds:"
    return _table(rows, head, lead,
                  "This lists what this area holds. It is not a claim about the rest of RouteMind —\n"
                  "if what you need is not here, go back to /v1/regions.")


def node(api: Api, path: str) -> str:
    d = api.json(path)
    rows = []
    # An entity can hold a body AND children at once — that is what one type bought. Asking for its
    # table and being told "(nothing here)" while a document sits on it is the table disagreeing with
    # the row that sent you: the row said `data`, this said empty. Its body is the first row.
    if str(d.get("body") or "").strip():
        # The node's own times, not an entry's — this row *is* the node. Written `_age(e)` at first,
        # against a loop variable that does not exist yet, which is a 500 on every node that has both
        # a body and children. Nothing in the dev repository has both; the shipped example does, and
        # a clean install caught it on the first boot.
        rows.append({"kind": KIND["file"], "address": path.rstrip("/") + "/body",
                     "why": "its own document", "age": _age(d), "whose": d.get("whose")})
    for e in (d.get("entries") or []):
        kind = {"data": KIND["file"], "empty": KIND["empty"]}.get(e.get("type"), KIND["table"])
        why = f"{e.get('name') or e.get('id')} — {e.get('one_liner') or e.get('description') or ''}"
        if kind == KIND["empty"]: why += "  (nothing written here yet)"
        rows.append({"kind": kind, "address": e.get("fetch") or "", "why": why, "age": _age(e), "whose": e.get("whose")})
    head = f"{d.get('name') or path}"
    return _table(rows, head, str(d.get("one_liner") or ""),
                  "This lists what this node holds. If what you need is not here, go back to /v1/regions.")


def _row(e: dict) -> dict:
    kind = {"data": KIND["file"], "empty": KIND["empty"]}.get(e.get("type"), KIND["table"])
    why = f"{e.get('name') or e.get('id')} — {e.get('one_liner') or ''}"
    if kind == KIND["empty"]: why += "  (nothing written here yet)"
    return {"kind": kind, "address": e.get("fetch") or "", "why": why, "age": _age(e),
            "whose": e.get("whose")}


def overlay_text(d: dict) -> str:
    """An overlay as an agent is handed it: every member's rows under its own heading, one set of
    columns across all of them, and the absence line — which is not optional. An overlay read as an
    inventory ("it is not in here, so it does not exist") is the one way this feature becomes a lie."""
    by = d.get("by") or {}
    head = [f"OVERLAY {d.get('id')} — {d.get('question') or ''}",
            f"{d.get('state')} · by {by.get('kind', '?')} {by.get('name', '')} · {d.get('rows', 0)} rows"]
    sections = d.get("sections") or []
    rows = [_row(e) for sec in sections for e in (sec.get("rows") or [])]
    addr_w = max([len(r["address"]) for r in rows] + [7])
    kind_w = max([len(r["kind"]) for r in rows] + [4])
    out = head + ["Your working set for this question. Pick from these rows; use each address as printed.", ""]
    out.append(f"  {'KIND'.ljust(kind_w)}  {'ADDRESS'.ljust(addr_w)}  WHY YOU WOULD PICK THIS ROW")
    for sec in sections:
        out.append(f"  ── {sec.get('member')} — {sec.get('why') or ''}")
        if sec.get("gone"):
            out.append("     (this member no longer resolves — it was moved or deleted)")
            continue
        sec_rows = [_row(e) for e in (sec.get("rows") or [])]
        if not sec_rows: out.append("     (nothing here)")
        for r in sec_rows:
            out.append(f"  {r['kind'].ljust(kind_w)}  {r['address'].ljust(addr_w)}  {_clip(r['why'], 110)}")
    out.append("")
    out.append("  table → knowledge_table({ path })    ·    file → knowledge_read({ path })")
    out.append("  narrow or widen → knowledge_overlay({ op: add | remove, id, address, why })")
    out.append("  Use the address exactly as printed above. Never build one.")
    out.append("")
    out.append(d.get("absence") or "Not finding it here means go back to /v1/regions — it does not mean it does not exist.")
    out.append("Go back to /v1/regions at most 3 times for one question; then say what you could not find.")
    out.append(f"When you answer, close it: knowledge_overlay({{ op: close, id: {d.get('id')}, outcome, used }}).")
    return "\n".join(out) + "\n"


def closed_text(d: dict) -> str:
    used = d.get("used") or []
    lines = [f"OVERLAY {d.get('id')} closed — {d.get('state')}"]
    for u in used:
        lines.append(f"  {u.get('how', '?').ljust(7)}  {u.get('address')}")
    if any(u.get("how") == "reached" for u in used):
        lines.append("  (reached = answered from somewhere the overlay never named — recorded as such)")
    return "\n".join(lines) + "\n"


def overlay_view(api: Api, path: str) -> str:
    return overlay_text(api.json(path))


def overlay_call(api: Api, args: dict) -> str:
    """One tool, five operations. `op` picks which; the rest are that operation's own fields."""
    op = str(args.get("op") or "").strip()
    oid = str(args.get("id") or "").strip()

    def need_id() -> str:
        if not oid: raise ApiError(f"op {op} needs the overlay's id — the one create printed")
        return oid

    if op == "create":
        return overlay_text(api.send("POST", "/v1/overlays", {
            "question": args.get("question") or "", "members": args.get("members") or [],
            "by": {"kind": "agent", "name": api.actor}}))
    if op == "get":
        return overlay_text(api.json(f"/v1/overlays/{urllib.parse.quote(need_id(), safe='')}"))
    if op in ("add", "remove"):
        return overlay_text(api.send("PATCH", f"/v1/overlays/{urllib.parse.quote(need_id(), safe='')}",
                                     {op: args.get("address") or "", "why": args.get("why") or ""}))
    if op == "close":
        return closed_text(api.send("POST", f"/v1/overlays/{urllib.parse.quote(need_id(), safe='')}/close",
                                    {"outcome": args.get("outcome") or "", "used": args.get("used") or []}))
    raise ApiError("op must be create | get | add | remove | close")


# ---- circuits: this session reading another RouteMind ---------------------------------------
#
# A *peer* links two backbones: declared in `peers.yaml`, reviewed, committed, tokens in the
# environment, and both sides configured. That weight is the point — it is a standing relationship
# between two ontologies, and it belongs in git.
#
# A *circuit* is the light version and a different thing: **this session** reading a remote
# backbone, for as long as this connection lasts. Nothing is written, nothing is committed, the
# remote is not told, and closing the client ends it. It exists because "let me look at theirs for a
# minute" should not require an operator, a restart, and a commit to two repositories.
#
# It needs no server change on either side. The remote already serves `/v1/export/…` to anyone with
# a valid `X-Peer-Token`, and that surface is built from the exported set rather than filtered on
# the way out — so a circuit can reach exactly what its token's owner decided to share and nothing
# else. The line it sees is `use_when` — one sentence, the same one they route on (2026-09-29).
#
# Read-only, and that is not a limitation to lift later. `server.py`: "a link is read-only — write
# to the backbone that owns it... Two ontologies that write to each other have been merged."
CIRCUITS: dict[str, dict] = {}


def _public_address(url: str) -> bool:
    """Would a token sent here cross a network nobody in this deployment controls?

    The same question `peers.public_address` asks, asked again here because a circuit sends the same
    kind of secret to the same kind of place, and a check that exists on one path and not the other
    protects nothing. Unresolvable is not public — a remote that is simply down should not produce a
    lecture about secrecy, which sends the reader looking in entirely the wrong place.
    """
    try:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "http": return False
        host = parts.hostname or ""
        if not host: return False
        try: infos = socket.getaddrinfo(host, None)
        except OSError: return False
        for info in infos:
            ip = ipaddress.ip_address(info[4][0])
            if not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved):
                return True
        return False
    except Exception:
        return False


def circuit_session(name: str) -> str:
    """The circuit's six-hour session, minted from the token the person gave, and held on it."""
    c = CIRCUITS[name]
    if c.get("session"): return c["session"]
    req = urllib.request.Request(c["url"] + "/v1/peers/token", data=b"", method="POST",
                                 headers={"X-Peer-Token": c["token"], "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            tok = str(json.loads(r.read().decode("utf-8")).get("token") or "")
    except urllib.error.HTTPError as e:
        raise ApiError(f"circuit {name}: {c['url']} refused the token (HTTP {e.code})", e.code)
    except urllib.error.URLError as e:
        raise ApiError(f"circuit {name} is unreachable at {c['url']} ({e.reason})")
    if not tok: raise ApiError(f"circuit {name}: no token came back from {c['url']}", 502)
    c["session"] = tok
    return tok


def circuit_fetch(name: str, path: str, accept: str) -> str:
    """One read across a circuit. `path` is written the way tables print it, beginning `/v1/`."""
    c = CIRCUITS.get(name)
    if not c: raise ApiError(f"no circuit named {name} — open one first", 404)
    tail = path[len("/v1/"):] if path.startswith("/v1/") else path.lstrip("/")
    url = c["url"] + "/v1/export/" + tail
    # A six-hour session rather than the token the person typed. The typed one opens the mint and
    # nothing else, so it appears once per circuit instead of on every hop of a walk — which matters
    # here more than anywhere, because a walk's reads are the ones that end up in a transcript.
    def go(tok):
        req = urllib.request.Request(url, headers={"Accept": accept, "X-Peer-Token": tok})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    try:
        return go(circuit_session(name))
    except urllib.error.HTTPError as e:
        # The far end restarted, or six hours passed mid-walk. Re-mint once: a restart over there
        # must cost a round trip, not the rest of the walk.
        if e.code == 401:
            c.pop("session", None)
            try:
                return go(circuit_session(name))
            except urllib.error.HTTPError as e2:
                detail = (e2.read().decode("utf-8", "replace") or "").strip()[:200]
                raise ApiError(f"circuit {name}: HTTP {e2.code} from /v1/export/{tail}"
                               + (f" — {detail}" if detail else ""), e2.code)
            except urllib.error.URLError as e2:
                raise ApiError(f"circuit {name} is unreachable at {c['url']} ({e2.reason})")
        detail = (e.read().decode("utf-8", "replace") or "").strip()[:200]
        raise ApiError(f"circuit {name}: HTTP {e.code} from /v1/export/{tail}"
                       + (f" — {detail}" if detail else ""), e.code)
    except urllib.error.URLError as e:
        raise ApiError(f"circuit {name} is unreachable at {c['url']} ({e.reason})")


def circuit_table(name: str, payload: str) -> str:
    """What a circuit returned, rendered as a table whose addresses go back through the circuit.

    Rewriting the addresses is the whole of it. The remote prints its own — `/v1/regions/expense` —
    and an agent that followed one verbatim would read this backbone's `expense` instead, silently
    and with an answer that looks entirely reasonable. Every row leaves here as
    `/v1/circuits/<name>/…`, so "use the address exactly as printed" stays true across a circuit.
    """
    try: d = json.loads(payload)
    except json.JSONDecodeError: return payload
    pre = f"/v1/circuits/{name}"
    rows = []
    for r in (d.get("regions") or []):
        # Its own `fetch` first; the source only as a fallback, in either spelling.
        src = (str(r.get("fetch") or "").rsplit("/", 1)[-1] if r.get("fetch") else "") or str(r.get("source") or r.get("id") or "").replace("_", "-")
        rows.append({"kind": KIND["table"], "address": f"{pre}/regions/{src}",
                     "why": r.get("use_when")
                            or r.get("description") or r.get("title") or ""})
    # A node's children come back under `entries`, each already carrying the address the remote
    # would print and whether anything is written there — the same shape the local tables are built
    # from. Guessed at `children`/`nodes` first, and the area table came out empty while the remote
    # had five rows: an empty table is the one wrong answer that looks like a fact.
    for e in (d.get("entries") or d.get("children") or d.get("nodes") or []):
        eid = e.get("id") or ""
        has = bool(e.get("has_body", True))
        kids = e.get("children")
        kind = KIND["table"] if kids else (KIND["file"] if has else KIND["empty"])
        tail = f"nodes/{eid}/body" if (kind == KIND["file"]) else f"nodes/{eid}"
        rows.append({"kind": kind, "address": f"{pre}/{tail}",
                     "why": e.get("one_liner") or e.get("name") or ""})
    # An area's own row points at the representative that holds it: `/v1/export/regions/<a>` answers
    # with the area's description, not its contents.
    if not rows and d.get("representative"):
        rows.append({"kind": KIND["table"], "address": f"{pre}/nodes/{d['representative']}",
                     "why": d.get("use_when") or d.get("advertises") or ""})
    title = f"CIRCUIT {name} — {d.get('name') or d.get('title') or 'a remote RouteMind'}"
    lead = ("Read-only, and only what its owner chose to let cross. The line on each row is the one "
            "they route on themselves — there is one sentence per area, not a separate one for "
            "outsiders.")
    return _table(rows, title, lead,
                  "Not finding something here does not mean they do not have it — it means they "
                  "did not export it. Ask them, do not conclude.")


def circuit_call(args: dict) -> str:
    op = str(args.get("op") or "").strip()
    if op == "list":
        if not CIRCUITS: return "No circuits are open."
        out = ["OPEN CIRCUITS", ""]
        for n, c in sorted(CIRCUITS.items()):
            out.append(f"  {n:<16} {c['url']}   → /v1/circuits/{n}/regions")
        return "\n".join(out) + ("\n\nThese last for this connection only. "
                                 "Nothing is written anywhere.")
    if op == "close":
        n = str(args.get("name") or "").strip()
        return f"Circuit {n} closed." if CIRCUITS.pop(n, None) else f"No circuit named {n}."
    if op != "open":
        return "op must be open, list or close."

    url = str(args.get("url") or "").strip().rstrip("/")
    token = str(args.get("token") or "").strip()
    name = str(args.get("name") or "").strip() or (urllib.parse.urlsplit(url).hostname or "remote")
    if not url or not token:
        return "url and token are both required — a circuit is a read into somebody else's ontology."
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        return f"name must be ascii kebab-case, got {name!r}"
    if _public_address(url):
        return (f"refusing to send a token to {url} — that is a public address over plain http, so "
                "the token would cross the wire in clear text. Use https, or a private address.")

    CIRCUITS[name] = {"url": url, "token": token}
    try:
        circuit_fetch(name, "/v1/regions", "application/json")
    except ApiError as e:
        CIRCUITS.pop(name, None)
        # Opened and immediately closed. A circuit that is listed but does not answer is worse than
        # none: the agent spends its hops discovering that, and the table said it was there.
        return f"Could not open circuit {name} — {e}\n\nNothing was kept."
    return (f"CIRCUIT {name} open  \u2192  {url}\n\n"
            f"  Read it at /v1/circuits/{name}/regions, then follow the addresses it prints.\n"
            "  It is read-only and holds only what its owner chose to let cross; the line on each\n"
            "  row is the one they route on themselves.\n"
            "  This lasts for this connection. Nothing was written on either side.")


WORKSPACE = "workspace"


def workspace_available(api: Api) -> bool:
    """Whether this install keeps a workspace area, asked rather than assumed.

    Same rule as overlays: no area, no tool, and nothing in the instructions about one. It also makes
    turning the feature on a single act a person takes deliberately — creating the area — rather than
    a flag somebody sets and forgets. An install that has not decided it wants machine-written notes
    does not get a tool that writes them.
    """
    try:
        rs = (api.json("/v1/regions") or {}).get("regions") or []
        return any((r.get("source") or r.get("id")) == WORKSPACE for r in rs)
    except ApiError:
        return False


def _slug(text: str, limit: int = 48) -> str:
    out = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return out[:limit].rstrip("-") or "entry"


def write_call(api: Api, args: dict) -> str:
    """Record what an agent just did, in the workspace area, under today's date.

    **The area is not a parameter.** Deciding where a subject lives changes the map, and the map is
    the text every walk reads before it chooses anything — one wrong row in it reached 39.7% of walks
    in the 700-question census, and the single miss in that census was one such row. So a machine
    writes a dated note and a person decides, later and by hand, which area it belongs to. Writing a
    note is cheap and reversible; changing the map is neither.
    """
    title = (args.get("title") or "").strip()
    body = (args.get("what_happened") or "").strip()
    if not title: return "title is required — one line naming what this is about."
    if not body: return "what_happened is required — this is the note itself."

    day = args.get("date") or _dt.date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        return f"date must be YYYY-MM-DD, got {day!r}"
    day_id = f"{WORKSPACE}-{day}"

    # One topic node per day, holding that day's entries. `topic` is the vocabulary's own word for a
    # node that groups and has nothing to read in itself, so the day needs no invented kind.
    try:
        api.json(f"/v1/nodes/{day_id}")
    except ApiError as e:
        if e.status != 404: raise
        api.send("POST", "/v1/nodes", {
            "region": WORKSPACE, "id": day_id, "kind": "topic", "name": day,
            "one_liner": f"What was recorded on {day}",
            "edges": [{"from": WORKSPACE, "rel": "CONSISTS_OF", "to": day_id}]})

    eid = f"{day_id}-{_slug(title)}"
    note = body
    sup = (args.get("supersedes") or "").strip()
    if sup:
        # In prose, not a field. The vocabulary has no SUPERSEDES relation, and the corpus convention
        # is that a document says so in its own words — which is also what the person who later files
        # this needs, since they will be reading it rather than querying it.
        note += f"\n\n## Supersedes\n\n{sup}"
    note += (f"\n\n---\n\nRecorded by an agent on {day}. Unfiled: nobody has decided which area this "
             f"belongs to, and nothing here has been checked for currency.")

    # Create, then write the body, then read it back.
    #
    # Three steps for what looks like one, and each is here because the shorter version failed. The
    # create accepts a `content` field and — through the web proxy at least — silently drops it,
    # leaving a node the tables mark `empty`: "nobody has written it yet. Do not fetch it." The tool
    # reported success. A note that cannot be read is worse than no note, because the agent that
    # wrote it believes the work is kept.
    made = api.send("POST", "/v1/nodes", {
        "region": WORKSPACE, "id": eid, "kind": args.get("kind") or "case", "name": title,
        "one_liner": (args.get("one_liner") or title)[:200],
        # `parent`, not only an edge. An edge relates two nodes; `parent` is what puts this one
        # *under* the day in the tree a walk descends. With the edge alone the day node listed
        # "(nothing here)" while the entry sat flat in the area.
        "parent": day_id,
        "content": note,
        "edges": [{"from": day_id, "rel": "CONSISTS_OF", "to": eid}]})
    got = (made or {}).get("id") or eid
    try:
        api.text(f"/v1/nodes/{got}/body")
    except ApiError as e:
        return (f"WROTE THE ROW BUT NOT THE NOTE  /v1/nodes/{got}\n  {e}\n\n"
                "  The entry exists and is empty, which tables advertise as `empty` — a row with\n"
                "  nothing behind it. Say so rather than treating the work as recorded.")

    # The service's own warnings about *this* write. It said, the first time, that a node with no
    # document "advertises as `empty`, which is a row with nothing behind it" — and the wrapper threw
    # that away and printed success.
    #
    # Only the ones naming what was just written. The service returns its whole repository health
    # report on every write: forty-eight lines here, about nodes nobody touched and fields nobody
    # fills. Printing all of it buries the one line that is about the caller, every time, in the
    # context of an agent that has work to do.
    mine = [w for w in ((made or {}).get("warnings") or []) if got in w or day_id in w]
    warn = "".join(f"\n  ! {w}" for w in mine)

    # The one-liner is echoed back on purpose. It is the only line a reader sees before opening this,
    # and an agent that has just spent a run inside one subject writes it in that run's vocabulary —
    # which is the exact failure this study measured at 0.028: a question in a person's words against
    # rows indexed by the words the writer happened to use.
    return ("RECORDED  /v1/nodes/" + got + f"\n  in {WORKSPACE}, under {day}" + warn + "\n\n"
            f"  one-liner:  {(args.get('one_liner') or title)[:200]}\n\n"
            "  That line is all a later reader sees before opening this. Would somebody who was not\n"
            "  in this run — searching in their own words, months from now — recognise it? If not,\n"
            "  write it again with a better one_liner; this note is unfiled and cheap\n"
            "  to replace.\n\n"
            "  It is not an answer to anything yet. Filing it into the area that owns its subject is\n"
            "  a person's edit, and that is when it gets a home and a statement of what it replaces.")


def overlays_available(api: Api) -> bool:
    """Whether this install keeps overlays. Asked, not assumed: 404 (an ontology without them) or 501
    (the store is not configured) means no, and then there is no tool and nothing in the instructions
    about one — an agent told about a tool that refuses every call learns the tool is broken."""
    # Anything else that goes wrong here (Knowledge unreachable) also means "not now": the next
    # connection asks again.
    try:
        api.json("/v1/overlays?state=open")
        return True
    except ApiError:
        return False


TABLE_ROUTES = (
    ("/v1/regions", hop0),
    ("/v1/regions/", area),
    ("/v1/nodes/", node),
    ("/v1/services/", node),
    ("/v1/overlays/", overlay_view),
)


# `/v1/peers/<backbone>/…` is an address on another backbone, relayed by this one. What follows the
# peer's name is an ordinary address, so the shape tests below run against that and the fetch runs
# against the whole thing. Rendering is identical on purpose: an area is an area, and which backbone
# it came from is already visible in the address the table printed.
_PEER = re.compile(r"^/v1/peers/[a-z][a-z0-9-]{0,30}(?=/)")


def _local(p: str) -> str:
    """The address with every peer prefix taken off, for deciding what kind of thing it is.

    Every, not one. Knowledge two backbones away arrives as `/v1/peers/ix/peers/branch/regions/x` —
    the path it came by, written into the address. Peeling one prefix leaves something that is still
    not a local shape, and the client then refuses to follow a row its own hop 0 printed.
    """
    while True:
        m = _PEER.match(p)
        if not m: return p
        p = "/v1" + p[m.end():]


def table_for(api: Api, path: str) -> str:
    p = (path or "/v1/regions").strip()
    if not p.startswith("/"): p = "/" + p
    if p in ("/v1/regions", "/v1/regions/", "/", ""): return hop0(api)
    shape = _local(p)
    for prefix, fn in TABLE_ROUTES[1:]:
        if shape.startswith(prefix) and len(shape) > len(prefix):
            return fn(api, p)
    raise ApiError(f"{p} is not a table address. Tables are /v1/regions, /v1/regions/<area>, "
                   f"/v1/nodes/<id>, /v1/services/<id>, and any of those behind /v1/peers/<backbone>/. "
                   f"Use an address a table printed.")


# The addresses that are tables. Reading is defined as "not one of these" rather than as a document
# shape, because the document shape is changing: the Knowledge unit is merging nodes and files into
# one kind of thing, after which a body is `/v1/nodes/<id>/body` and `/files/` disappears. A reader
# that required `/files/` would have refused every address the new tables print. This is the
# consumer half of that move, done first and on its own — nothing here depends on the new shape
# arriving, and nothing breaks if it never does.
TABLE_SHAPES = (
    re.compile(r"^/v1/regions/?$"),
    re.compile(r"^/v1/regions/[^/]+/?$"),
    re.compile(r"^/v1/nodes/[^/]+/?$"),
    re.compile(r"^/v1/services/[^/]+/?$"),
    re.compile(r"^/v1/overlays/[^/]+/?$"),
)


def read_for(api: Api, path: str) -> str:
    p = (path or "").strip()
    if not p.startswith("/v1/"):
        raise ApiError(f"{p!r} is not an address from Knowledge. Use one a table printed.")
    if any(rx.match(_local(p)) for rx in TABLE_SHAPES):
        raise ApiError(f"{p} is a table, not a document — call knowledge_table with it.")
    return api.text(p)


# ── MCP ───────────────────────────────────────────────────────────────────────

PLACE_TOOL = {
    "name": "knowledge_place",
    "description": "Put a new document into RouteMind by walking the routing table to its place — "
                   "the same walk a question takes, not a scan of the corpus for a likely spot. "
                   "`open` with the document (name, one_liner, optional aliases and content) prints "
                   "hop 0 with, on every row, which of the document's words its sentence shares. "
                   "`step` with an address from that table descends one hop and prints the next "
                   "table the same way; at every hop below the top you may `here` instead, and the "
                   "document becomes a child of the node whose table you are reading. `none` at hop "
                   "0 means no area advertises such things, and the answer is a new area, not a "
                   "hiding place. `here` writes the document under the parent reached and then walks "
                   "back up: every ancestor whose line does not say this gets a proposal to widen it "
                   "by the document's own one_liner, stopping at the first ancestor that already "
                   "covers it — route aggregation. If nothing covers it to hop 0, the area's sentence "
                   "is proposed; whether the area is exported is reported and never changed here.",
    "inputSchema": {"type": "object", "required": ["op"], "properties": {
        "op": {"type": "string", "enum": ["open", "step", "here", "list", "close"]},
        "name": {"type": "string", "description": "open: the document's name"},
        "one_liner": {"type": "string", "description": "open: one sentence, the line a table will print for it"},
        "aliases": {"type": "array", "items": {"type": "string"}, "description": "open: the names people use for it"},
        "content": {"type": "string", "description": "open: the body, Markdown"},
        "id": {"type": "string", "description": "step/here/close: the placement id `open` returned"},
        "pick": {"type": "string", "description": "step: an address the last table printed, or `none`"}}},
}

PLACEMENTS: dict[str, dict] = {}

# ── the walk: invariant 1, in code ────────────────────────────────────────────
# Every walk starts at hop 0. Until 2026-10-06 that was a sentence in a tool description, and an agent
# quoted it while breaking it. Now this server remembers, for the session it serves, whether hop 0 has
# been served: `knowledge_table` with no address serves it and starts a walk, and every call below hop
# 0 — an area's table, a node's table, a document, a circuit's table — is refused until it has been.
#
# No id is handed to the agent. One MCP server serves one agent session, so the walk is simply the
# current one: the agent opens hop 0, walks, and opens hop 0 again for its next question, which ends
# the walk before it. A version that issued a walk id the agent had to pass on every call enforced
# exactly this and no more — it could not stop an agent answering from memory either — and cost every
# call an argument nobody could explain (operator, 2026-10-07). A walk also ends after
# `KNOWLEDGE_WALK_TTL` seconds (600).
#
# Enforced here and not in the service: this is the agent's only door, and the rule is about agents —
# a screen or a curl reads tables freely. The footprint (docs/FOOTPRINT.md) records every walk under
# the id the backbone gives it, out of the agent's sight.
WALKS: dict[str, dict] = {}
CURRENT: dict = {"walk": None}
WALK_TTL = float(os.environ.get("KNOWLEDGE_WALK_TTL") or 600)
_walk_n = [0]


def open_walk(api: Api, how: str) -> str:
    """A new walk from hop 0. The walk before it is over — here, and on the record, as `abandoned`:
    nothing said it was answered, and the next question started."""
    prev = WALKS.get(CURRENT["walk"] or "")
    if prev and not prev["ended"]:
        prev["ended"] = "a new hop 0 was served"
        close_walk(api, prev["id"], "abandoned", "a new question started")
    wid, remote = "", False
    try:
        d = api.send("POST", "/v1/walks", {"question": "", "how": how})
        wid, remote = str(d.get("id") or ""), bool(d.get("id"))
    except ApiError as e:
        if "501" not in str(e) and "not configured" not in str(e):
            sys.stderr.write(f"knowledge-mcp: footprint not recorded — {e}\n")
    if not wid:
        _walk_n[0] += 1; wid = f"w{_walk_n[0]}"
    WALKS[wid] = {"id": wid, "how": how, "opened": time.time(), "ended": None, "calls": 0, "remote": remote}
    CURRENT["walk"] = wid
    return wid


def report(api: Api, wid: str, op: str, address: str, why: str) -> None:
    """One step onto the record. A step that cannot be recorded does not fail the read — but it is
    said, because a footprint with a hole in it is worse than none when somebody replays it."""
    w = WALKS.get(wid)
    if not w or not w.get("remote"): return
    try: api.send("POST", f"/v1/walks/{wid}/steps", {"op": op, "address": address, "why": why})
    except ApiError as e:
        sys.stderr.write(f"knowledge-mcp: step not recorded on {wid} — {e}\n")


def close_walk(api: Api, wid: str, outcome: str, why: str) -> None:
    w = WALKS.get(wid)
    if not w or not w.get("remote"): return
    try: api.send("POST", f"/v1/walks/{wid}/close", {"outcome": outcome, "why": why})
    except ApiError as e:
        sys.stderr.write(f"knowledge-mcp: walk {wid} not closed on the record — {e}\n")


def need_why(args: dict, what: str) -> str:
    """The reason for a step, required. The footprint exists so a person can see what the agent was
    thinking, not only where it went."""
    why = str(args.get("why") or "").strip()
    if not why:
        raise ApiError(f"{what} needs `why` — one line on why this row, for the record of this walk "
                       f"(docs/FOOTPRINT.md). Say what in the row's line made you open it.")
    return why[:200]


BACK_TO_HOP0 = ("Every walk starts at hop 0: call knowledge_table with no address first — it lists the "
                "areas — then follow the addresses its rows print.")


def require_walk(what: str) -> dict:
    """The current walk, or the refusal that says how to start one."""
    w = WALKS.get(CURRENT["walk"] or "")
    if not w or w["ended"]:
        raise ApiError(f"{what}: hop 0 has not been opened for this question. {BACK_TO_HOP0}")
    if time.time() - w["opened"] > WALK_TTL:
        w["ended"] = f"it is older than {int(WALK_TTL)}s"
        close_walk(api_for_close[0], w["id"], "abandoned", w["ended"]) if api_for_close[0] else None
        raise ApiError(f"{what}: the walk has expired ({w['ended']}). {BACK_TO_HOP0}")
    w["calls"] += 1
    return w


api_for_close: list = [None]

# Tools that exist and are off by default. `KNOWLEDGE_TOOLS_EXTRA=overlay,write` turns them on.
_extra = {x.strip() for x in str(os.environ.get("KNOWLEDGE_TOOLS_EXTRA") or "").split(",") if x.strip()}
OPTIONAL = {"overlay": "overlay" in _extra, "write": "write" in _extra}


def place_call(api: Api, args: dict) -> str:
    """The placement walk, one op at a time. State is the walk's path and the addresses the last
    table printed — a pick that was not printed is refused, the same discipline every table asks."""
    op = str(args.get("op") or "").strip()
    if op == "list":
        if not PLACEMENTS: return "No placement is open."
        return "\n".join(f"  {k}  {p['doc']['name']}  at {p['at']}  path {' → '.join(p['path']) or '(hop 0)'}"
                         for k, p in PLACEMENTS.items())
    if op == "open":
        doc = {"name": str(args.get("name") or "").strip(), "one_liner": str(args.get("one_liner") or "").strip(),
               "aliases": [str(a) for a in (args.get("aliases") or [])], "content": str(args.get("content") or "")}
        if not doc["name"] or not doc["one_liner"]:
            raise ApiError("open needs `name` and `one_liner` — the line is what every table will print for it")
        pid = f"p{len(PLACEMENTS) + 1}"
        PLACEMENTS[pid] = {"doc": doc, "path": [], "at": "/v1/regions", "printed": []}
        return _place_hop(api, pid)
    pid = str(args.get("id") or "").strip()
    p = PLACEMENTS.get(pid)
    if not p: raise ApiError(f"no placement {pid!r} is open — `open` one, or `list`")
    if op == "close":
        del PLACEMENTS[pid]; return f"placement {pid} closed; nothing was written."
    if op == "step":
        pick = str(args.get("pick") or "").strip().rstrip("/")
        if pick == "none":
            if p["at"] == "/v1/regions":
                del PLACEMENTS[pid]
                return ("No area at hop 0 advertises such things, so there is nowhere to place this without hiding it.\n"
                        "What is needed is a new area: a representative and one sentence saying when to come.\n"
                        f"A candidate for that sentence is the document's own line:\n  {p['doc']['one_liner']}\n"
                        "Nothing was written.")
            return _place_here(api, pid)
        if pick not in p["printed"]:
            raise ApiError(f"{pick} is not an address the last table printed. Pick one of: {', '.join(p['printed'])} — or `none`.")
        p["path"].append(pick); p["at"] = pick
        return _place_hop(api, pid)
    if op == "here":
        if p["at"] == "/v1/regions": raise ApiError("a document cannot be placed at hop 0 — step into an area first, or say `none`")
        return _place_here(api, pid)
    raise ApiError(f"op must be open · step · here · list · close (got {op!r})")


def _place_hop(api: Api, pid: str) -> str:
    p = PLACEMENTS[pid]
    d = api.send("POST", "/v1/place", {"at": p["at"], "doc": p["doc"], "path": p["path"]})
    p["printed"] = [r["address"] for r in d.get("rows") or []]
    out = [f"ROUTEMIND — placing {p['doc']['name']!r}  [{pid}]",
           f"  terms   : {', '.join(d.get('terms') or []) or '(none)'}",
           f"  walked  : {' → '.join(p['path']) or '(hop 0)'}", ""]
    rows = d.get("rows") or []
    if rows:
        w = max(len(r["address"]) for r in rows)
        out.append(f"  {'ADDRESS':<{w}}  SHARES              LINE")
        for r in rows:
            ev = r.get("evidence") or {}
            shares = ", ".join(dict.fromkeys(ev.get("terms", []) + ev.get("names", []))) or "—"
            out.append(f"  {r['address']:<{w}}  {shares[:18]:<18}  {(r.get('line') or '')[:90]}")
    else:
        out.append("  (no rows — this node has no children yet)")
    out.append("")
    here = d.get("here")
    if here:
        out.append(f"  `here` places it as a child of {here['parent']} in {here['region']}.")
        prop = d.get("propagation") or {}
        if prop.get("proposals"):
            out.append("  Advertising it would widen: " + "; ".join(f"{q['label']} ({q['scope']})" for q in prop["proposals"])
                       + (f" — then stops at {prop['stop_at']['label']}, whose line already covers it ({', '.join(prop['stop_at']['hits'])})" if prop.get("stop_at") else
                          " — nothing above covers it, so this reaches hop 0" + (f"; the area is export: {'yes' if (d.get('export') or {}).get('export') else 'no'}" if d.get("export") else "")))
        elif prop.get("stop_at"):
            out.append(f"  Nothing to advertise: {prop['stop_at']['label']} already covers it ({', '.join(prop['stop_at']['hits'])}).")
        out.append("  `step` with an address above goes one hop deeper; `none` here means place it here.")
    else:
        out.append("  Pick the area whose sentence covers this document (`step` with its address), or `none` if no area does.")
    return "\n".join(out)


def _place_here(api: Api, pid: str) -> str:
    p = PLACEMENTS[pid]
    d = api.send("POST", "/v1/place", {"at": p["at"], "doc": p["doc"], "path": p["path"]})
    here = d.get("here") or {}
    body = {"name": p["doc"]["name"], "one_liner": p["doc"]["one_liner"], "region": here.get("region"),
            "parent": here.get("parent"), "aliases": p["doc"].get("aliases") or [], "content": p["doc"].get("content") or ""}
    made = api.send("POST", "/v1/nodes", body)
    nid = made.get("id") or made.get("node", {}).get("id") or "?"
    out = [f"PLACED {p['doc']['name']!r} as {nid}, child of {here.get('parent')} in {here.get('region')}",
           f"  walked  : {' → '.join(p['path'])}", ""]
    prop = d.get("propagation") or {}
    queued = []
    for q in prop.get("proposals") or []:
        pb = {"scope": q["scope"], "before": q["before"], "after": q["after"], "why": q["why"],
              **({"entity": q["entity"]} if q["scope"] == "entity" else {"region": q["region"]})}
        try:
            r = api.send("POST", "/v1/curator/proposals", pb)
            queued.append(f"  queued   {q['label']} ({q['scope']}): {r.get('id', '?')}\n           → {q['after'][:110]}")
        except ApiError as e:
            queued.append(f"  refused  {q['label']} ({q['scope']}): {e}")
    if queued:
        out.append("Advertising, as proposals for review — not applied here:")
        out += queued
        if prop.get("stop_at"): out.append(f"  stops at {prop['stop_at']['label']}, whose line already covers it.")
        elif prop.get("reaches_hop0"):
            ex = d.get("export") or {}
            out.append(f"  reaches hop 0. The area is export: {'yes' if ex.get('export') else 'no'} — exporting is a separate decision, not taken here.")
    elif prop.get("stop_at"):
        out.append(f"Nothing to advertise: {prop['stop_at']['label']} already covers it ({', '.join(prop['stop_at']['hits'])}).")
    del PLACEMENTS[pid]
    return "\n".join(out)


TOOLS = [
    {"name": "knowledge_table",
     "description": "Fetch a routing table from Knowledge: a list of what is there and where to go "
                    "next. Call it with no arguments to get the list of areas — that is where every "
                    "search starts. Each row prints the exact address that fetches it; use those "
                    "verbatim and never construct one.",
     "inputSchema": {"type": "object", "properties": {
         "path": {"type": "string",
                  "description": "An address a table printed: /v1/regions (the areas), "
                                 "/v1/regions/<area>, /v1/nodes/<id> or /v1/services/<id>. "
                                 "Omit for the list of areas."},
         "why": {"type": "string",
                 "description": "Below hop 0, required: one line on why you are opening this row — what in "
                                "its line made you choose it. Recorded on the walk (docs/FOOTPRINT.md)."}}}},
    {"name": "knowledge_read",
     "description": "Read one document from Knowledge, by the address a table printed for it. "
                    "Returns the document as written.",
     "inputSchema": {"type": "object", "properties": {
         "path": {"type": "string", "description": "The address a table printed for this document."},
         "why": {"type": "string", "description": "Required: one line on why this document. Recorded on the walk."}},
         "required": ["path", "why"]}},
]

OVERLAY_TOOL = {
    "name": "knowledge_overlay",
    "description": "Your working set for one question (a VRF). After reading the list of areas, create "
                   "one from the rows the question belongs to, each with the reason you picked it. It "
                   "prints one table holding all of them — work from that. Add or remove members as you "
                   "narrow, each with a reason. If the answer is not in it, go back to the list of areas "
                   "(at most 3 times) — not finding it here does not mean it does not exist. When you "
                   "answer or give up, close it with the addresses you actually used.",
    "inputSchema": {"type": "object", "required": ["op"], "properties": {
        "op": {"type": "string", "enum": ["create", "get", "add", "remove", "close"]},
        "question": {"type": "string", "description": "create: the question this set is for, as asked"},
        "members": {"type": "array", "description": "create: addresses a table printed, each with why",
                    "items": {"type": "object", "required": ["address", "why"], "properties": {
                        "address": {"type": "string"}, "why": {"type": "string"}}}},
        "id": {"type": "string", "description": "get / add / remove / close: the overlay's id"},
        "address": {"type": "string", "description": "add / remove: an address a table printed"},
        "why": {"type": "string", "description": "add / remove: the reason"},
        "outcome": {"type": "string", "enum": ["answered", "not_found"], "description": "close"},
        "walk": {"type": "string", "description": "close: the walk id hop 0 printed for this question. "
                                                  "Required to close as not_found — only someone who has "
                                                  "seen the whole list may say something is not here."},
        "used": {"type": "array", "items": {"type": "string"},
                 "description": "close: every address you actually took the answer from, member or not"}}}}


WRITE_TOOL = {
    "name": "knowledge_write",
    "description": "Record what you just did, so it is not lost when this session ends. Use it at the "
                   "end of a piece of work — a decision you reached, a case the rules did not settle "
                   "and how you settled it, a procedure you worked out. It writes a dated note into "
                   "the workspace area.\n\n"
                   "You do not choose where it goes. Everything lands in `workspace` under today's "
                   "date, and a person files it into the area that owns its subject later. That is "
                   "deliberate: which area a subject belongs to is part of the routing table every "
                   "search reads first, and moving it is a decision with consequences a note does "
                   "not have.\n\n"
                   "What you write here is NOT an answer to anything yet. It is unreviewed, it is not "
                   "checked against what it might replace, and nothing will route a later question to "
                   "it. If you learned that a rule is now different, say so in `supersedes` — the "
                   "person filing this will need it and will not be able to reconstruct it.",
    "inputSchema": {"type": "object", "required": ["title", "what_happened"], "properties": {
        "title": {"type": "string",
                  "description": "One line naming what this is about, in the words somebody looking "
                                 "for it later would use — not the words this run happened to use"},
        "what_happened": {"type": "string",
                          "description": "The note itself, in markdown. What the situation was, what "
                                         "you did, and what you concluded"},
        "one_liner": {"type": "string",
                      "description": "The single line a reader sees before opening this. Defaults to "
                                     "the title"},
        "supersedes": {"type": "string",
                       "description": "If this changes or replaces something already written down, "
                                      "what — in your own words, naming the document if you know it"},
        "kind": {"type": "string",
                 "enum": ["case", "rule", "procedure", "form", "table", "system", "role", "deadline"],
                 "description": "Defaults to `case` — a situation the rules did not settle and what "
                                "was actually done. That is usually what a run produces"},
        "date": {"type": "string", "description": "YYYY-MM-DD. Defaults to today"}}}}


CIRCUIT_TOOL = {
    "name": "knowledge_circuit",
    "description": "Read another RouteMind for the length of this connection. Give it the address "
                   "and token somebody handed you, and their shared areas appear alongside this "
                   "backbone's — you walk them the same way, with the addresses their tables "
                   "print.\n\n"
                   "It is read-only, and it holds only what its owner chose to let cross. The line "
                   "on each row is the one that backbone routes on itself — one sentence per area, "
                   "written by its owner about their own map rather than about yours.\n\n"
                   "Nothing is written on either side and nothing outlives this connection. This is "
                   "not the same as linking two backbones, which is a standing arrangement somebody "
                   "configures and commits; this is you borrowing a reader's view of theirs.",
    "inputSchema": {"type": "object", "required": ["op"], "properties": {
        "op": {"type": "string", "enum": ["open", "list", "close"]},
        "url": {"type": "string", "description": "open: the remote RouteMind's address, e.g. https://kb.example.com"},
        "token": {"type": "string", "description": "open: the read token its owner gave you"},
        "name": {"type": "string",
                 "description": "open: a short name to address it by (ascii kebab-case; defaults to "
                                "the host). close: which one to close"}}}}


class Server:
    def __init__(self, api: Api):
        api_for_close[0] = api
        self.api = api
        self._overlays = None
        self._workspace = None

    def workspace(self) -> bool:
        if self._workspace is None: self._workspace = workspace_available(self.api)
        return self._workspace

    def overlays(self) -> bool:
        if self._overlays is None: self._overlays = overlays_available(self.api)
        return self._overlays

    def instructions(self) -> str:
        """What the model is told about this server before it has looked at any tool.

        The tool description was meant to carry the list of areas, on the reasoning that it is the
        one text every client shows the model. Measured in Claude Code, that is false: it loads MCP
        tools lazily, so what the model sees up front is two names and nothing else. Asked "an order
        sent by SlowPost is six business days late, what do I do?", it never called this server,
        grepped the repository, found nothing and answered from general knowledge — while the answer
        sat in an area whose condition was literally "an order has not arrived".

        Server instructions are delivered at initialize, before tools, and a client shows them
        whether or not the tools are loaded yet. So the areas go here too: the list is what tells a
        model that a question belongs to this domain at all, which a tool name cannot.
        """
        try:
            areas = hop0(self.api)
        except ApiError as e:
            return ("RouteMind is this team's domain knowledge base, and it is not reachable right now "
                    f"({e}). Questions about the domain it covers will need it.")
        intro = ("RouteMind is this team's own domain knowledge base. It holds facts that are specific to "
                 "this domain and are not in general knowledge or in any repository.\n\n"
                 "When a question touches anything in the list below, consult Knowledge BEFORE answering "
                 "from general knowledge or searching files. A generic answer to a question this list "
                 "covers is a wrong answer.\n\n")
        if OPTIONAL["overlay"] and self.overlays():
            # Switched on (KNOWLEDGE_TOOLS_EXTRA=overlay): the operator's flow, docs/OVERLAY.md. The
            # budget for going back lives here because only the agent can count it.
            return intro + ("How to work a question:\n"
                            "  1. Start at hop 0: knowledge_table with no arguments — the list below. Pick every\n"
                            "     row the question belongs to.\n"
                            "  2. knowledge_overlay { op: create, question, members: [{address, why}] } — your working\n"
                            "     set. It prints one table holding all of them.\n"
                            "  3. Work from that table: knowledge_table / knowledge_read on the addresses it prints,\n"
                            "     each with a one-line `why`. Add or remove members as you narrow, each with a reason.\n"
                            "  4. Not in it? Come back to this list — at most 3 times. Not finding something in your\n"
                            "     working set does not mean Knowledge lacks it; only this list can say that.\n"
                            "  5. knowledge_overlay { op: close, id, outcome: answered | not_found, used: [addresses] }.\n\n"
                            + areas)
        # Off by default (2026-10-07): one way to work, the walk from hop 0.
        return intro + ("Every question starts at hop 0: call knowledge_table with no arguments, pick the "
                        "row whose sentence matches, and follow the addresses the tables print — "
                        "knowledge_table for a table, knowledge_read for a document, each with a one-line "
                        "`why`. Only this list may tell you something is absent; a smaller table only "
                        "tells you it is not in there.\n\n" + areas)

    def tools(self) -> list[dict]:
        """The tool list, with the areas of this domain written into the first description.

        An MCP client has no way to put anything in a system prompt, and the whole design rests on
        an agent seeing the areas *before* it decides anything. A tool description is the one piece
        of text every client does show the model, so that is where the list goes. If Knowledge is
        unreachable the tools are still listed — an agent that cannot see the areas can still ask
        for them, and the error it gets back says what is wrong.
        """
        tools = [dict(t) for t in TOOLS]
        try:
            tools[0]["description"] += "\n\n" + hop0(self.api)
        except ApiError as e:
            tools[0]["description"] += f"\n\n(The area list could not be fetched: {e})"
        tools.append(dict(PLACE_TOOL))
        tools.append(dict(CIRCUIT_TOOL))
        # Off unless switched on (operator, 2026-10-07: "Simple is best"). The code stays; an agent
        # sees four tools — table, read, place, circuit — unless the install asks for more.
        if OPTIONAL["overlay"] and self.overlays(): tools.append(dict(OVERLAY_TOOL))
        if OPTIONAL["write"] and self.workspace(): tools.append(dict(WRITE_TOOL))
        return tools

    def call(self, name: str, args: dict) -> tuple[str, bool]:
        try:
            if name == "knowledge_place": return place_call(self.api, args), False
            if name == "knowledge_circuit": return circuit_call(args), False
            path = str(args.get("path") or "").strip()
            # Hop 0 itself: the one table that needs no walk, because it is where one begins.
            if name == "knowledge_table" and path.rstrip("/") in ("", "/", "/v1/regions"):
                open_walk(self.api, "knowledge_table")
                return hop0(self.api), False
            # Everything below hop 0 belongs to the walk hop 0 opened — invariant 1 — and every step
            # is recorded with the reason the agent gave — invariant 11.
            if name in ("knowledge_table", "knowledge_read"):
                w = require_walk(f"{name} {path}")
                why = need_why(args, f"{name} {path}")
                report(self.api, w["id"], "table" if name == "knowledge_table" else "read", path, why)
            # An address into an open circuit is answered by the circuit, not this backbone. The
            # agent never composes one: it follows what a circuit's own tables printed, the same
            # discipline as every other address here.
            if name in ("knowledge_table", "knowledge_read") and path.startswith("/v1/circuits/"):
                rest = path[len("/v1/circuits/"):]
                cname, _, tail = rest.partition("/")
                doc = name == "knowledge_read"
                body = circuit_fetch(cname, "/v1/" + tail,
                                     "text/markdown" if doc else "application/json")
                return (body if doc else circuit_table(cname, body)), False
            if name == "knowledge_table": return table_for(self.api, path), False
            if name == "knowledge_read":  return read_for(self.api, path), False
            if name == "knowledge_overlay" and OPTIONAL["overlay"] and self.overlays():
                out = overlay_call(self.api, args)
                if str(args.get("op") or "") == "close":
                    w = WALKS.get(CURRENT["walk"] or "")
                    outcome = str(args.get("outcome") or "")
                    if w and not w["ended"]:
                        close_walk(self.api, w["id"], outcome if outcome in ("answered", "not_found") else "answered",
                                   f"overlay closed {outcome or 'answered'}")
                        w["ended"] = "its overlay was closed"
                return out, False
            if name == "knowledge_write" and OPTIONAL["write"] and self.workspace(): return write_call(self.api, args), False
            return f"No such tool: {name}", True
        except ApiError as e:
            return str(e), True

    def handle(self, msg: dict) -> dict | None:
        method, mid = msg.get("method"), msg.get("id")
        params = msg.get("params") or {}

        def ok(result): return {"jsonrpc": "2.0", "id": mid, "result": result}

        if method == "initialize":
            asked = str(params.get("protocolVersion") or "")
            return ok({"protocolVersion": asked or PROTOCOL_FALLBACK,
                       "capabilities": {"tools": {}, "prompts": {}},
                       "serverInfo": {"name": "knowledge", "version": "0.1.0"},
                       "instructions": self.instructions()})
        if method in ("notifications/initialized", "initialized", "notifications/cancelled"):
            return None                                   # notifications carry no id and take no reply
        if method == "ping": return ok({})
        if method == "tools/list": return ok({"tools": self.tools()})
        if method == "tools/call":
            text, is_error = self.call(str(params.get("name") or ""), params.get("arguments") or {})
            return ok({"content": [{"type": "text", "text": text}], "isError": is_error})
        if method == "prompts/list":
            return ok({"prompts": [
                {"name": "knowledge_start",
                 "description": "The areas of this domain, and how to search them."},
                # Arguments, so a client can offer them as fields rather than making somebody
                # compose a tool call. A circuit is the one thing here a person starts deliberately:
                # everything else an agent reaches for on its own, and this is somebody saying
                # "read theirs too, now".
                {"name": "circuit",
                 "description": "Open a circuit to another RouteMind and read what it shares — for "
                                "this connection only, writing nothing on either side.",
                 "arguments": [
                     {"name": "url", "description": "the remote RouteMind's address, "
                                                    "e.g. https://kb.example.com", "required": True},
                     {"name": "token", "description": "the token its owner gave you", "required": True},
                     {"name": "name", "description": "what to call it here — ascii kebab-case; "
                                                     "defaults to the host", "required": False}]}]})
        if method == "prompts/get":
            # By name. This used to answer hop 0 whatever was asked for, which was correct while
            # there was one prompt and would have made a second one silently return the first.
            which = str(params.get("name") or "knowledge_start")
            args = params.get("arguments") or {}
            if which == "circuit":
                url, token = str(args.get("url") or "").strip(), str(args.get("token") or "").strip()
                if not url or not token:
                    body = ("A circuit needs the remote's address and a token its owner gave you.\n\n"
                            "  url:    https://kb.example.com   ·   token: the one you were handed\n"
                            "  name:   optional — what to call it here")
                else:
                    # Opened here rather than handed to the model as an instruction to open: the
                    # person typed the address and the token, and a prompt that asks an agent to
                    # please make a tool call is one more place the two can disagree.
                    body = circuit_call({"op": "open", "url": url, "token": token,
                                         "name": str(args.get("name") or "").strip()})
                return ok({"description": "A circuit to another RouteMind",
                           "messages": [{"role": "user", "content": {"type": "text", "text": body}}]})
            if which != "knowledge_start":
                return {"jsonrpc": "2.0", "id": mid,
                        "error": {"code": -32602, "message": f"Unknown prompt: {which}"}}
            try: body = hop0(self.api)
            except ApiError as e: body = str(e)
            return ok({"description": "Where to start in Knowledge",
                       "messages": [{"role": "user", "content": {"type": "text", "text": body}}]})
        if mid is None: return None
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Unknown method: {method}"}}


def _utf8_stdio() -> None:
    """This stream is UTF-8 in both directions, whatever the machine's locale says.

    Python picks the *locale* encoding for a pipe, and an MCP server's stdout is always a pipe. On
    Windows that is the ANSI code page — cp1252 on a Western install, cp949 on a Korean one, cp932 on
    a Japanese one — and none of the three can encode `—` or `→`. Both appear in the text this server
    sends before it has answered anything: the area list travels in `instructions`, which goes out
    with the `initialize` reply. So on any Windows with Python 3.14 or older (UTF-8 mode became the
    default only in 3.15) this died on the MCP handshake with a UnicodeEncodeError, before a single
    tool call — and it is not about Korean data, an English install fails on the same two characters.
    Reading has the same problem in reverse: a client sending a non-ASCII `question` or `why` for an
    overlay would arrive as mojibake or not decode at all.

    `newline="\n"` on the way out because text mode on Windows turns every `\n` into `\r\n`, and the
    framing here is one JSON object per line. Most clients tolerate the stray `\r`; the protocol does
    not promise they will, and there is nothing to gain by sending it.

    Wrapped, because a caller may hand `serve()` its own streams — the checks do — and those are not
    required to be reconfigurable."""
    for stream, kw in ((sys.stdin, {}), (sys.stdout, {"newline": "\n"})):
        try: stream.reconfigure(encoding="utf-8", **kw)
        except Exception: pass


def serve(api: Api, stdin=sys.stdin, stdout=sys.stdout) -> None:
    """One JSON object per line, in and out. Anything this process writes to stdout that is not a
    response corrupts the stream, so every diagnostic goes to stderr."""
    if stdin is sys.stdin and stdout is sys.stdout: _utf8_stdio()
    server = Server(api)
    for line in stdin:
        line = line.strip()
        if not line: continue
        try: msg = json.loads(line)
        except Exception:
            stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
                                     "error": {"code": -32700, "message": "Parse error"}}) + "\n")
            stdout.flush(); continue
        try: reply = server.handle(msg)
        except Exception as e:                             # a crash must not take the session down
            sys.stderr.write(f"knowledge-mcp: {type(e).__name__}: {e}\n")
            reply = {"jsonrpc": "2.0", "id": msg.get("id"),
                     "error": {"code": -32603, "message": f"{type(e).__name__}: {e}"}}
        if reply is not None:
            stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            stdout.flush()


def main() -> None:
    p = argparse.ArgumentParser(description="RouteMind over MCP (stdio).")
    p.add_argument("--api", default=os.environ.get("KNOWLEDGE_API", "http://localhost:8080/api/knowledge"),
                   help="The v1 root: the web app's Knowledge API (http://localhost:8080/api/knowledge), "
                        "or an ontology directly (http://localhost:8100/v1)")
    p.add_argument("--actor", default=os.environ.get("KNOWLEDGE_ACTOR", "mcp"),
                   help="The name recorded on anything this connection causes to be written.")
    a = p.parse_args()
    sys.stderr.write(f"knowledge-mcp: api={a.api} actor={a.actor}\n")
    serve(Api(a.api, a.actor))


if __name__ == "__main__":
    main()
