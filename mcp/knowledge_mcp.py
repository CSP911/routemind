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
        # An install in token mode (docs/AUTH.md) refuses writes without its secret, and the server had
        # no way to send one: an agent could read but not place, and every walk went unrecorded
        # (2026-10-10). KNOWLEDGE_TOKEN from the environment, or from the .env of this checkout.
        tok = _env_value("KNOWLEDGE_TOKEN")
        if tok: headers["Authorization"] = f"Bearer {tok}"
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, method=method, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            detail, payload = "", None
            try:
                payload = json.loads(body)
                detail = (payload.get("detail") or payload.get("error") or "")
            except Exception: detail = body[:400]
            raise ApiError(f"HTTP {e.code} from {path}" + (f" — {detail}" if detail else ""), e.code,
                           payload if isinstance(payload, dict) else None)
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
    def __init__(self, message: str, status: int | None = None, payload: dict | None = None):
        super().__init__(message)
        self.status = status
        self.payload = payload or {}      # the refusal whole, where it carries more than a sentence


# ── the tables an agent is handed ─────────────────────────────────────────────
#
# Three columns and a footer, identical at every hop, because a model that has learned to read one
# table has then learned to read all of them. `KIND` names the tool to call, so choosing a row and
# choosing a tool are one decision rather than two.

def _clip(text: str, limit: int | None) -> str:
    """One line, emphasis marks taken out; cut at `limit` with `…`, or whole when `limit` is None."""
    s = " ".join(str(text or "").replace("*", "").replace("`", "").split())
    return s if limit is None or len(s) <= limit else s[: limit - 1] + "…"


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


def _table(rows: list[dict], title: str, lead: str, foot_absence: str | None, clip: int | None = 100) -> str:
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
    out = [title, lead, ""]
    head = f"  {'KIND'.ljust(kind_w)}  {'ADDRESS'.ljust(addr_w)}  "
    if age_w: head += f"{'AGE'.ljust(age_w)}  "
    out.append(head + "WHY YOU WOULD PICK THIS ROW")
    for r in rows:
        line = f"  {r['kind'].ljust(kind_w)}  {r['address'].ljust(addr_w)}  "
        if age_w: line += f"{ages[id(r)].ljust(age_w)}  "
        out.append(line + _clip(r["why"], clip))
    out.append("")
    if age_w:
        # Said once, under the table, because a column of `3y / 2d` with nothing explaining it is
        # read as one number twice. The second half is the one that answers "should I look for
        # something newer"; the first says whether this path has been settled or was just laid down.
        out.append("  AGE is how long this route has been here / when its document last changed.")
        out.append("  An old route over a recently changed document is current. An old route over a")
        out.append("  document that has not moved is the one to ask about before quoting it.")
        if any((r.get("age") or "") in ("—", "") or "?" in (r.get("age") or "") for r in rows):
            out.append("  `—` is not known here — its history could not be read. That is not the same as new.")
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
             "age": _age(r)}
            for r in (d.get("regions") or [])]
    absence = (
        "Nothing outside this list exists in RouteMind. This list is the grounds on which you may say\n"
        "something is absent — no smaller table is.")
    # A circuit opened in this session reads another backbone. Without a line here hop 0 said nothing
    # existed outside it while the circuit stood open, and the agent had no way in but to guess that
    # the circuit's table was reachable (2026-10-10).
    if CIRCUITS:
        absence += ("\n\nCircuits open in this session — other backbones, read-only. Their tables are not\n"
                    "part of this list, and what they do not hold says nothing about what exists:\n" +
                    "\n".join(f"  table  /v1/circuits/{n}/regions   {c['url']}" for n, c in CIRCUITS.items()))
    # Whole, never clipped (operator, 2026-10-08). `use_when` is the one sentence an agent chooses an
    # area by, and its last clause is as likely as its first to be the one this question matches —
    # cut at 100 characters, five of six areas here lost theirs behind a `…`.
    return _table(
        rows,
        "ROUTEMIND — the areas of this domain",
        "Pick the row whose condition matches the question, then fetch it. One step, then read.",
        absence,
        clip=None,
    )


def area(api: Api, path: str) -> str:
    d = api.json(path)
    rows = []
    for e in (d.get("entries") or []):
        kind = {"data": KIND["file"], "empty": KIND["empty"]}.get(e.get("type"), KIND["table"])
        why = f"{e.get('name') or e.get('id')} — {e.get('one_liner') or ''}"
        if kind == KIND["empty"]: why += "  (nothing written here yet)"
        rows.append({"kind": kind, "address": e.get("fetch") or "", "why": why, "age": _age(e)})
    head = f"{d.get('key') or path} — {d.get('advertises') or ''}".strip(" —")
    lead = (f"When to be here: {d['use_when']}" if d.get("use_when") else "") or "What this area holds:"
    # Whole rows, never clipped (2026-10-10): a row cut at 100 characters lost the clause that said
    # what the document held, and the agent concluded "not in RouteMind" without opening it.
    return _table(rows, head, lead,
                  "This lists what this area holds. It is not a claim about the rest of RouteMind —\n"
                  "if what you need is not here, go back to /v1/regions. Before saying a detail is not\n"
                  "covered, read the documents in this table that could hold it.", clip=None)


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
                     "why": "its own document", "age": _age(d)})
    for e in (d.get("entries") or []):
        kind = {"data": KIND["file"], "empty": KIND["empty"]}.get(e.get("type"), KIND["table"])
        why = f"{e.get('name') or e.get('id')} — {e.get('one_liner') or e.get('description') or ''}"
        if kind == KIND["empty"]: why += "  (nothing written here yet)"
        rows.append({"kind": kind, "address": e.get("fetch") or "", "why": why, "age": _age(e)})
    head = f"{d.get('name') or path}"
    return _table(rows, head, str(d.get("one_liner") or ""),
                  "This lists what this node holds. If what you need is not here, go back to /v1/regions.\n"
                  "Before saying a detail is not covered, read the documents in this table that could hold it.", clip=None)


def _row(e: dict) -> dict:
    kind = {"data": KIND["file"], "empty": KIND["empty"]}.get(e.get("type"), KIND["table"])
    why = f"{e.get('name') or e.get('id')} — {e.get('one_liner') or ''}"
    if kind == KIND["empty"]: why += "  (nothing written here yet)"
    return {"kind": kind, "address": e.get("fetch") or "", "why": why, "age": _age(e)}


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
            out.append(f"  {r['kind'].ljust(kind_w)}  {r['address'].ljust(addr_w)}  {r['why']}")
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
# A *circuit* is **this session** reading another RouteMind, for as long as this connection lasts —
# the one way left to read another backbone since standing links were retired (2026-10-08). Nothing is written, nothing is committed, the
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

    A circuit sends the enrolment key; over plain http to a public address that is a bearer secret
    in clear text on the wire. Unresolvable is not public — a remote that is simply down should not produce a
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


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """A circuit follows no redirect. The session rides in a header, and following one sent it to
    whatever host the far end named — past the plain-http check, which only ever saw the address the
    circuit was opened with (found 2026-10-10)."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, f"redirect to {newurl} refused — a circuit does not follow redirects", headers, fp)


_CIRCUIT_OPENER = urllib.request.build_opener(_NoRedirect)


def circuit_session(name: str) -> str:
    """The circuit's six-hour session, minted from the token the person gave, and held on it."""
    c = CIRCUITS[name]
    if c.get("session"): return c["session"]
    req = urllib.request.Request(c["url"] + "/v1/peers/token", data=b"", method="POST",
                                 headers={"X-Peer-Token": c["token"], "Accept": "application/json"})
    try:
        with _CIRCUIT_OPENER.open(req, timeout=30) as r:
            tok = str(json.loads(r.read().decode("utf-8")).get("token") or "")
    except urllib.error.HTTPError as e:
        # What each refusal means for the person who has to fix it, rather than "refused the token"
        # for all of them — a 501 is the far end having no key at all, a 404 is the wrong address.
        why = {401: "refused the key — check it is the far end's KNOWLEDGE_CIRCUIT_TOKEN",
               501: "has no circuit key set (KNOWLEDGE_CIRCUIT_TOKEN in its .env is empty), so nothing can be read from it",
               404: "has no circuit endpoint at that address — give the install's own address, e.g. http://host:8080, without /api/knowledge",
               }.get(e.code, f"refused the circuit (HTTP {e.code})")
        if 300 <= e.code < 400: why = f"answered with a redirect, which a circuit does not follow (HTTP {e.code})"
        raise ApiError(f"circuit {name}: {c['url']} {why}", e.code)
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
        with _CIRCUIT_OPENER.open(req, timeout=30) as r:
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
        if 300 <= e.code < 400:
            raise ApiError(f"circuit {name}: {c['url']} answered with a redirect, which a circuit does not follow (HTTP {e.code})", e.code)
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
    # From the address when none is given: `127.0.0.1:9330` and `kb.example.com` have dots, and a dot
    # is not allowed in a name, so the bare host refused every address but `localhost` (2026-10-10).
    parts = urllib.parse.urlsplit(url)
    auto = re.sub(r"[^a-z0-9]+", "-", f"{parts.hostname or 'remote'}{'-' + str(parts.port) if parts.port else ''}".lower()).strip("-")
    name = str(args.get("name") or "").strip() or (auto[:40].strip("-") or "remote")
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
            f"  Read it at /v1/circuits/{name}/regions, then follow the addresses it prints — after your own\n"
            "  hop 0 (knowledge_table, no path), which now lists this circuit; every walk starts there.\n"
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
            "one_liner": f"What was recorded on {day}"})

    eid = f"{day_id}-{_slug(title)}"
    note = body
    sup = (args.get("supersedes") or "").strip()
    if sup:
        # In prose, not a field. The corpus convention is that a document says so in its own words — which is also what the person who later files
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
        # `parent` is what puts this one *under* the day in the tree a walk descends.
        "parent": day_id,
        "content": note})
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
    ("/v1/overlays/", overlay_view),
)


def table_for(api: Api, path: str) -> str:
    p = (path or "/v1/regions").strip()
    if not p.startswith("/"): p = "/" + p
    if p in ("/v1/regions", "/v1/regions/", "/", ""): return hop0(api)
    for prefix, fn in TABLE_ROUTES[1:]:
        if p.startswith(prefix) and len(p) > len(prefix):
            return fn(api, p)
    raise ApiError(f"{p} is not a table address. Tables are /v1/regions, /v1/regions/<area>, "
                   f"or /v1/nodes/<id>. "
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
    re.compile(r"^/v1/overlays/[^/]+/?$"),
)


def read_for(api: Api, path: str) -> str:
    p = (path or "").strip()
    if not p.startswith("/v1/"):
        raise ApiError(f"{p!r} is not an address from Knowledge. Use one a table printed.")
    if any(rx.match(p) for rx in TABLE_SHAPES):
        raise ApiError(f"{p} is a table, not a document — call knowledge_table with it.")
    return api.text(p)


# ── MCP ───────────────────────────────────────────────────────────────────────

PLACE_TOOL = {
    "name": "knowledge_place",
    "description": "Put a new document into RouteMind by walking the routing table to its place — "
                   "the same walk a question takes, not a scan of the corpus for a likely spot. "
                   "`open` with the document (name, one_liner, optional content) prints hop 0. Read "
                   "the lines and choose. `step` with an address from that table descends one hop and "
                   "prints the next table; at every hop below the top you may `here` instead, and the "
                   "document becomes a child of the node whose table you are reading. `none` at hop "
                   "0 means no area advertises such things; then `here` with `area` makes the area, "
                   "its sentence and the document in one commit. "
                   "`here` is one commit of several decisions. The document is one; the lines over it "
                   "are the rest: every table the change alters has a line above it, and each must be "
                   "decided — `keep` it, or `reword` it. Refused, `here` prints those lines with the "
                   "table before and after; call it again with the decisions added. Decisions may also "
                   "make a holder (`create` with a `ref` like $h, and `parent` $h on the document or on "
                   "siblings you `move` under it — how a wide table is folded), `move` a sibling, "
                   "`write` a body, `delete` a leaf. The order of decisions does not matter. "
                   "`dry_run` shows all of this without writing. "
                   "Keep a line when its topic still covers what is under it — an area's sentence says when to come "
                   "there, not a list of every document, so do not append a clause for each new one. "
                   "A new version of a rule: create it, and move the old one under a holder named for the old "
                   "versions — {op: create, ref: $prev, name: 'Earlier versions', one_liner: …, parent: <holder>}, "
                   "{op: move, id: <old>, parent: $prev}. Two or more related documents in a wide table: fold them "
                   "under a holder the same way — and give the holder a line that names what is under it, not a "
                   "section label: a weaker model choosing by a holder's line stops short when the line says little "
                   "(eval/depth). `content` is what the person gave you, as they gave it — never add "
                   "rules, numbers or conditions they did not state; ask if it is unclear.",
    "inputSchema": {"type": "object", "required": ["op"], "properties": {
        "op": {"type": "string", "enum": ["open", "step", "here", "list", "close"]},
        "name": {"type": "string", "description": "open: the document's name"},
        # Measured 2026-10-10: given a one-paragraph policy to file, the agent wrote the paragraph itself
        # as the line. The table then prints the answer instead of when to open the page, and the next
        # walker reads a summary in place of the document.
        "one_liner": {"type": "string", "description": "open: one sentence, the line a table will print for it — what a "
                      "reader would come to it for (\"how many days a week may be worked from home, and how to book it\"), "
                      "not its content restated; the content goes in `content`"},
        "content": {"type": "string", "description": "open: the body, Markdown"},
        "kind": {"type": "string", "description": "open, optional: a kind from this backbone's vocabulary. Left out, the document takes the kind its documented siblings mostly have"},
        "id": {"type": "string", "description": "step/here/close: the placement id `open` returned"},
        "pick": {"type": "string", "description": "step: an address the last table printed, or `none`"},
        "why": {"type": "string", "description": "here: one line on what this change is for — it becomes the commit"},
        "parent": {"type": "string", "description": "here: put the document under this instead of the node reached — a ref like $h the decisions create, or an address the last table printed"},
        "decisions": {"type": "array", "description": "here: the other decisions, each {op: keep|reword|create|move|write|delete, …}: "
                      "keep {id, field, why?} · reword {id, field, after, before?} · create {ref, name, one_liner, content?, parent} · "
                      "move {id, parent} · write {id, content} · delete {id}. field is one_liner, or use_when for an area's face.",
                      "items": {"type": "object"}},
        "expose": {"type": "array", "items": {"type": "string"}, "description": "here: ids this change knowingly makes readable through a circuit (moved into an exported area)"},
        "area": {"type": "object", "description": "here at hop 0: the new area — {source, name, one_liner, use_when}; the document goes under its face",
                 "properties": {"source": {"type": "string"}, "name": {"type": "string"}, "one_liner": {"type": "string"}, "use_when": {"type": "string"}}},
        "dry_run": {"type": "boolean", "description": "here: show the impact and the lines to decide without writing"}}},
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


def open_walk(api: Api, how: str, question: str = "") -> str:
    """A new walk from hop 0. The walk before it is over — here, and on the record, as `abandoned`:
    nothing said it was answered, and the next question started."""
    prev = WALKS.get(CURRENT["walk"] or "")
    if prev and not prev["ended"]:
        prev["ended"] = "a new hop 0 was served"
        close_walk(api, prev["id"], "abandoned", "a new question started")
    wid, remote = "", False
    try:
        # A check walking a real install marks its walks, so the map and its history show the walks
        # agents took rather than forty "the check walks here" (2026-10-10). Still recorded.
        d = api.send("POST", "/v1/walks", {"question": str(question or "").strip()[:300], "how": how,
                                           **({"check": True} if os.environ.get("KNOWLEDGE_WALK_CHECK") else {})})
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
               "content": str(args.get("content") or ""), "kind": str(args.get("kind") or "").strip()}
        if not doc["name"] or not doc["one_liner"]:
            raise ApiError("open needs `name` and `one_liner` — the line is what every table will print for it")
        pid = f"p{len(PLACEMENTS) + 1}"
        PLACEMENTS[pid] = {"doc": doc, "path": [], "at": "/v1/regions", "printed": []}
        # Its first table is hop 0, so it opens a walk like hop 0 does: reading a document while
        # placing was refused with "hop 0 has not been opened" while hop 0 was on screen (2026-10-10).
        open_walk(api, "knowledge_place", f"file “{doc['name']}”")
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
                return ("No area at hop 0 advertises such things, so there is nowhere to place this without hiding it.\n"
                        "What is needed is a new area: a face and one sentence saying when to come. Make it with\n"
                        f"  here {{ id: {pid}, area: {{ source, name, one_liner, use_when }}, why }}\n"
                        "and the document goes under it, in the same commit. A candidate for the sentence is the\n"
                        f"document's own line:\n  {p['doc']['one_liner']}\n"
                        "Nothing was written yet; `close` to drop it.")
            return _place_here(api, pid, args)
        if pick not in p["printed"]:
            raise ApiError(f"{pick} is not an address the last table printed. Pick one of: {', '.join(p['printed'])} — or `none`.")
        p["path"].append(pick); p["at"] = pick
        # Each hop of a placement is a step of its walk, like a question's — the record showed hop 0
        # and nothing after it (2026-10-10).
        w = CURRENT.get("walk")
        if w: report(api, w, "table", pick, f"placing “{p['doc']['name']}” — chose this row")
        return _place_hop(api, pid)
    if op == "here":
        if p["at"] == "/v1/regions" and not isinstance(args.get("area"), dict):
            raise ApiError("a document cannot be placed at hop 0 — step into an area first, or make one: `here` with `area` {source, name, one_liner, use_when}")
        return _place_here(api, pid, args)
    raise ApiError(f"op must be open · step · here · list · close (got {op!r})")


def _place_hop(api: Api, pid: str) -> str:
    p = PLACEMENTS[pid]
    d = api.send("POST", "/v1/place", {"at": p["at"]})
    p["printed"] = [r["address"] for r in d.get("rows") or []]
    p["revision"] = d.get("revision")      # what the decisions will rest on
    out = [f"ROUTEMIND — placing {p['doc']['name']!r}  [{pid}]",
           f"  its line: {p['doc']['one_liner']}",
           f"  walked  : {' → '.join(p['path']) or '(hop 0)'}", ""]
    rows = d.get("rows") or []
    if rows:
        w = max(len(r["address"]) for r in rows)
        out.append(f"  {'ADDRESS':<{w}}  LINE")
        for r in rows:
            out.append(f"  {r['address']:<{w}}  {r.get('line') or ''}")
    else:
        out.append("  (no rows — this node has no children yet)")
    out.append("")
    here = d.get("here")
    # A wide table is the one a person would fold. Said once, not enforced: whether these rows
    # belong together is the judgement the agent is here to make.
    if len(rows) > WIDE_TABLE:
        out.append(f"  This table is wide ({len(rows)} rows). If some of these belong together, `here` can fold them:")
        out.append("  create a holder ({op: create, ref: $h, name, one_liner, parent: <this node>}) and move them under it.")
    if here:
        out.append(f"  `here` places it as a child of {here['parent']} in {here['region']} — with `why`, and a decision for each line over it.")
        out.append("  `step` with an address above goes one hop deeper.")
    else:
        out.append("  Pick the area whose sentence covers this document (`step` with its address), or `none` if no area does.")
    return "\n".join(out)


WIDE_TABLE = 9


def _place_here(api: Api, pid: str, args: dict) -> str:
    """The write, as one change set: the document, and every decision the caller added. Refused with
    the lines over it undecided, the refusal prints them with the tables before and after — the
    next call carries the decisions. Nothing is partly written."""
    p = PLACEMENTS[pid]
    doc = p["doc"]
    why = str(args.get("why") or "").strip() or f"place {doc['name']}"
    decisions = list(args.get("decisions") or [])
    for d in decisions:
        if not isinstance(d, dict): raise ApiError("every decision is an object: {op: keep|reword|create|move|write|delete, …}")
    area = args.get("area") if p["at"] == "/v1/regions" else None
    if area is not None:
        for k in ("source", "name", "one_liner", "use_when"):
            if not str(area.get(k) or "").strip(): raise ApiError(f"area.{k} is required — a new area is a face and the sentence hop 0 prints for it")
        decisions.append({"op": "create", "ref": "$area", "name": area["name"], "one_liner": area["one_liner"],
                          "parent": None, "area": area["source"], "use_when": area["use_when"]})
        parent = "$area"
    else:
        d = api.send("POST", "/v1/place", {"at": p["at"]})
        here = d.get("here") or {}
        parent = str(args.get("parent") or "").strip() or here.get("parent")
        if parent and parent.startswith("/v1/nodes/"): parent = parent[len("/v1/nodes/"):]
        if not parent: raise ApiError("nowhere to place it — step into an area first")
    decisions.insert(0, {"op": "create", "ref": "$doc", "name": doc["name"], "one_liner": doc["one_liner"],
                         "content": doc.get("content") or "", "parent": parent,
                         **({"kind": doc["kind"]} if doc.get("kind") else {})})
    body = {"why": why, "decisions": decisions, "expose": list(args.get("expose") or []),
            **({"base": p["revision"]} if p.get("revision") else {}), "dry_run": bool(args.get("dry_run"))}
    try:
        res = api.send("POST", "/v1/changes", body)
    except ApiError as e:
        v = (e.payload or {}).get("values") or {}
        imp = v.get("impact")
        if imp and (e.payload or {}).get("reason") in ("undecided", "exposure"):
            return "\n".join([f"NOT WRITTEN — {e.payload.get('error') or e.payload.get('detail') or e}", "", *_impact_lines(imp, v.get("ids") or {}), "",
                               "Call `here` again with the same arguments and `decisions` carrying, for each line above:",
                               "  {op: keep, id, field, why}  — its text still covers what is under it now, or",
                               "  {op: reword, id, field, after} — the sentence it should print instead.",
                               *(["  and `expose: [ids]` for what this knowingly makes readable through a circuit."] if imp.get("unacknowledged") else [])])
        if (e.payload or {}).get("reason") == "stale":
            raise ApiError(f"{e} — the tables this walk read have changed; `close` it and walk again")
        raise
    if res.get("dry_run"):
        imp = res.get("impact") or {}
        return "\n".join([f"DRY RUN — nothing written. {'It applies as it is.' if res.get('applies') else 'It does not apply yet:'}", "",
                           *_impact_lines(imp, res.get("ids") or {})])
    if res.get("queued"):
        # The set is filed; a person decides it. The placement ends here, because filing the same
        # document again some other way (keeping the sentence instead of rewording it) placed it
        # twice over — once now, once more if the queued set were ever accepted (2026-10-10).
        del PLACEMENTS[pid]
        return "\n".join([f"QUEUED {res['queued']} — {res.get('message')}", "", *_impact_lines(res.get("impact") or {}, res.get("ids") or {}),
                           "", "Nothing is written until a person accepts it in the review queue, and this placement is",
                           "closed: do not file the document again another way. Tell the person it is waiting there."])
    del PLACEMENTS[pid]
    ids = res.get("ids") or {}
    imp = res.get("impact") or {}
    w = CURRENT.get("walk")
    if w and WALKS.get(w) and not WALKS[w]["ended"]:
        WALKS[w]["ended"] = "placed"
        close_walk(api, w, "answered", f"placed as {ids.get('$doc', '?')}, commit {str(res.get('revision') or '')[:10]}")
    out = [f"PLACED {doc['name']!r} as {ids.get('$doc', '?')} — commit {str(res.get('revision') or '')[:10]}",
           f"  walked  : {' → '.join(p['path']) or '(hop 0)'}"]
    for k, v in ids.items():
        if k != "$doc": out.append(f"  made    : {k} = {v}")
    for l in imp.get("lines", []):
        out.append(f"  line    : {l['id']}.{l['field']} {l['decided']}" + (f" — was: {l['was']}" if l.get("was") else ""))
    for e in imp.get("exposure", []):
        out.append(f"  {'exposed' if e['to'] else 'withdrawn'}: {e['id']}")
    return "\n".join(out)


def _impact_lines(imp: dict, ids: dict) -> list[str]:
    """The impact, printed: each table that changes, before and after, and the line over it."""
    out = []
    if ids: out.append("  ids     : " + ", ".join(f"{k} = {v}" for k, v in ids.items()))
    for t in imp.get("tables", []):
        owner = "hop 0" if t["owner"] == "@hop0" else t["owner"]
        out.append(f"  table of {owner}:")
        before = {r["id"]: r["line"] for r in t.get("before", [])}; after = {r["id"]: r["line"] for r in t.get("after", [])}
        for k in sorted(set(before) | set(after)):
            mark = "  " if before.get(k) == after.get(k) else ("- " if k not in after else ("+ " if k not in before else "~ "))
            out.append(f"    {mark}{k}  {(after.get(k) if k in after else before.get(k)) or ''}"[:160])
    for l in imp.get("lines", []):
        out.append(f"  line {l['id']}.{l['field']}: {l['decided'] or 'UNDECIDED'}  — now reads: {l['text']!r}"[:220])
    for e in imp.get("exposure", []):
        out.append(f"  {'newly readable through a circuit' if e['to'] else 'no longer readable through a circuit'}: {e['id']}")
    for c in imp.get("carried", []):
        out.append(f"  carried along: {c['id']} (under {c['under']})")
    return out


TOOLS = [
    {"name": "knowledge_table",
     "description": "Fetch a routing table from RouteMind: a list of what is there and where to go "
                    "next. Call it with no path (and `question`) to get the list of areas — that is where every "
                    "question starts. With a path, `why` is required. Each row prints the exact address that fetches it; use those "
                    "verbatim and never construct one.",
     "inputSchema": {"type": "object", "properties": {
         "path": {"type": "string",
                  "description": "An address a table printed: /v1/regions (the areas), "
                                 "/v1/regions/<area> or /v1/nodes/<id>. "
                                 "Omit for the list of areas."},
         "why": {"type": "string",
                 "description": "Below hop 0, required: one line on why you are opening this row — what in "
                                "its line made you choose it. Recorded on the walk (docs/FOOTPRINT.md)."},
         "question": {"type": "string",
                      "description": "At hop 0 (no path): the person's question, verbatim, in their language. Recorded "
                                     "on the walk, so a person replaying it can see what was asked."}}}},
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
                 "When a question touches anything in the list below, consult RouteMind BEFORE answering "
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
        # "The list below is a preview" because the agent read addresses off it and called them
        # straight away, and the server refused: hop 0 had not been opened (seen 2026-10-10).
        return intro + ("Every question starts at hop 0: call knowledge_table with no path — with "
                        "`question` set to what you are answering — even though the list is below: this "
                        "list is a preview, and the server refuses any table under it until that call is "
                        "made. Every new question starts at hop 0 again, even in the same conversation. "
                        "Then pick the row whose sentence matches, and follow the addresses the tables print — "
                        "knowledge_table for a table, knowledge_read for a document, each with a one-line "
                        "`why`. Only this list may tell you something is absent; a smaller table only "
                        "tells you it is not in there — and before saying a detail is not covered, read the "
                        "documents in the table you are in that could hold it.\n\n"
                        # Without this a model asked to "add this to RouteMind" did not know the place
                        # tool existed — Claude Code loads tools lazily — and tried to write files into
                        # the repository by hand (2026-10-10).
                        "To add, update or replace a document in RouteMind, use knowledge_place — never edit "
                        "files in the repository directly. Write what the person gave you, as they gave it; "
                        "do not add rules, numbers or conditions they did not state.\n\n" + areas)

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
        place = dict(PLACE_TOOL)
        try:
            # The kinds this backbone's vocabulary has, so the agent can choose one: left to a default,
            # documents came out as "topic" — a holder's kind — four times in nine (2026-10-10).
            kinds = [k for k in (self.api.json("/v1/vocab").get("kinds") or []) if isinstance(k, dict) and k.get("id")]
            if kinds:
                place["description"] += (" Kinds in this backbone (pass `kind` on open): " +
                                         "; ".join(f"{k['id']} — {str(k.get('desc') or '').strip()}" for k in kinds) + ".")
        except ApiError:
            pass
        tools.append(place)
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
                open_walk(self.api, "knowledge_table", str(args.get("question") or ""))
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
    # The client went away. A walk left open showed as "walking" on the map for an hour and then as
    # abandoned, though the session had simply ended (2026-10-10).
    w = WALKS.get(CURRENT.get("walk") or "")
    if w and not w["ended"]:
        w["ended"] = "the session ended"
        close_walk(api, w["id"], "ended", "the session ended")


def _env_value(key: str) -> str:
    """A setting from the environment, else from the `.env` beside this repository (the last line
    wins, as compose reads it)."""
    if os.environ.get(key): return os.environ[key].strip()
    val = ""
    env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    try:
        for line in open(env, encoding="utf-8"):
            k, _, v = line.strip().partition("=")
            if k.strip() == key: val = v.strip().strip("'\"")
    except OSError:
        pass
    return val


def _default_api() -> str:
    """Where this checkout's install answers: `KNOWLEDGE_API` if set, else the port in the `.env` beside
    this repository, else 8080. `.mcp.json` no longer names a port, so install.sh does not rewrite a
    tracked file — that left every checkout on another port dirty, a `git pull` that could refuse, and
    a port changed in `.env` by hand (as docs/INSTALL.md says to) pointing Claude Code at the old one."""
    if os.environ.get("KNOWLEDGE_API"): return os.environ["KNOWLEDGE_API"]
    port = ""
    env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    try:
        for line in open(env, encoding="utf-8"):
            k, _, v = line.strip().partition("=")
            if k.strip() == "WEB_PORT" and v.strip().strip("'\""): port = v.strip().strip("'\"")   # the last one wins, as compose reads it
    except OSError:
        pass
    return f"http://localhost:{port if port.isdigit() else '8080'}/api/knowledge"


def main() -> None:
    p = argparse.ArgumentParser(description="RouteMind over MCP (stdio).")
    p.add_argument("--api", default=_default_api(),
                   help="The v1 root: the web app's Knowledge API (http://localhost:8080/api/knowledge), "
                        "or an ontology directly (http://localhost:8100/v1)")
    p.add_argument("--actor", default=os.environ.get("KNOWLEDGE_ACTOR", "mcp"),
                   help="The name recorded on anything this connection causes to be written.")
    a = p.parse_args()
    sys.stderr.write(f"knowledge-mcp: api={a.api} actor={a.actor}\n")
    serve(Api(a.api, a.actor))


if __name__ == "__main__":
    main()
