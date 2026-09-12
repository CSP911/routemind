#!/usr/bin/env python3
"""RouteMind over MCP — so any MCP-capable agent can read this ontology.

    knowledge-mcp --api http://localhost:8080/api/knowledge

Two tools, because navigating this ontology is two operations and nothing else:

    knowledge_table(path)   fetch a routing table — a list of what is there and where to go next
    knowledge_read(path)    fetch one document

and a third where the install keeps overlays (docs/OVERLAY.md):

    knowledge_overlay(op)   the working set for one question — create it from what hop 0 pointed at,
                            narrow it, close it with what was used

An agent never composes an address. Every row a table prints carries the exact `path` that fetches
it, which is why the structure can move without breaking a caller. Addresses assembled by the caller
broke once already, silently, when documents moved one level down.

Stdlib only, and one file, for the same reason the ontology service is: it has to be trivially
runnable by someone who has not set this project up.

What an agent is handed here is the same shape the map previews and the same shape a web console
gets. There is one advertisement, and every engine reads it.
"""
from __future__ import annotations

import argparse
import json
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


def _table(rows: list[dict], title: str, lead: str, foot_absence: str | None) -> str:
    if not rows:
        # An empty table still has to say what its emptiness means. Without the footer, "(nothing
        # here)" is the strongest claim on the page and the only one with no scope attached — an
        # agent can read it as "this does not exist" while six other areas go unlooked-at.
        tail = f"\n\n{foot_absence}\n" if foot_absence else "\n"
        return f"{title}\n{lead}\n\n  (nothing here){tail}"
    addr_w = max(len(r["address"]) for r in rows)
    kind_w = max(len(r["kind"]) for r in rows)
    out = [title, lead, ""]
    out.append(f"  {'KIND'.ljust(kind_w)}  {'ADDRESS'.ljust(addr_w)}  WHY YOU WOULD PICK THIS ROW")
    for r in rows:
        out.append(f"  {r['kind'].ljust(kind_w)}  {r['address'].ljust(addr_w)}  {_clip(r['why'], 110)}")
    out.append("")
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
             "why": r.get("use_when") or r.get("description") or r.get("title") or ""}
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
        rows.append({"kind": kind, "address": e.get("fetch") or "", "why": why})
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
        rows.append({"kind": KIND["file"], "address": path.rstrip("/") + "/body",
                     "why": "its own document"})
    for e in (d.get("entries") or []):
        kind = {"data": KIND["file"], "empty": KIND["empty"]}.get(e.get("type"), KIND["table"])
        why = f"{e.get('name') or e.get('id')} — {e.get('one_liner') or e.get('description') or ''}"
        if kind == KIND["empty"]: why += "  (nothing written here yet)"
        rows.append({"kind": kind, "address": e.get("fetch") or "", "why": why})
    head = f"{d.get('name') or path}"
    return _table(rows, head, str(d.get("one_liner") or ""),
                  "This lists what this node holds. If what you need is not here, go back to /v1/regions.")


def _row(e: dict) -> dict:
    kind = {"data": KIND["file"], "empty": KIND["empty"]}.get(e.get("type"), KIND["table"])
    why = f"{e.get('name') or e.get('id')} — {e.get('one_liner') or ''}"
    if kind == KIND["empty"]: why += "  (nothing written here yet)"
    return {"kind": kind, "address": e.get("fetch") or "", "why": why}


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


def table_for(api: Api, path: str) -> str:
    p = (path or "/v1/regions").strip()
    if not p.startswith("/"): p = "/" + p
    if p in ("/v1/regions", "/v1/regions/", "/", ""): return hop0(api)
    for prefix, fn in TABLE_ROUTES[1:]:
        if p.startswith(prefix) and len(p) > len(prefix):
            return fn(api, p)
    raise ApiError(f"{p} is not a table address. Tables are /v1/regions, /v1/regions/<area>, "
                   f"/v1/nodes/<id> and /v1/services/<id>. Use an address a table printed.")


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
    if any(rx.match(p) for rx in TABLE_SHAPES):
        raise ApiError(f"{p} is a table, not a document — call knowledge_table with it.")
    return api.text(p)


# ── MCP ───────────────────────────────────────────────────────────────────────

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
                                 "Omit for the list of areas."}}}},
    {"name": "knowledge_read",
     "description": "Read one document from Knowledge, by the address a table printed for it. "
                    "Returns the document as written.",
     "inputSchema": {"type": "object", "properties": {
         "path": {"type": "string", "description": "The address a table printed for this document."}},
         "required": ["path"]}},
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
        "used": {"type": "array", "items": {"type": "string"},
                 "description": "close: every address you actually took the answer from, member or not"}}}}


class Server:
    def __init__(self, api: Api):
        self.api = api
        self._overlays = None

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
        if not self.overlays():
            return intro + ("Call knowledge_table with no arguments, pick the matching row, and follow the "
                            "addresses it prints.\n\n" + areas)
        # The operator's flow (docs/OVERLAY.md): list the targets from hop 0, draw the working set,
        # work inside it. The budget for going back lives here because only the agent can count it.
        return intro + ("How to work a question:\n"
                        "  1. From the list below, pick every row the question belongs to.\n"
                        "  2. knowledge_overlay { op: create, question, members: [{address, why}] } — your working\n"
                        "     set. It prints one table holding all of them.\n"
                        "  3. Work from that table: knowledge_table / knowledge_read on the addresses it prints.\n"
                        "     Add or remove members as you narrow, each with a reason.\n"
                        "  4. Not in it? Come back to this list — at most 3 times. Not finding something in your\n"
                        "     working set does not mean Knowledge lacks it; only this list can say that.\n"
                        "  5. knowledge_overlay { op: close, id, outcome: answered | not_found, used: [addresses] }.\n\n"
                        + areas)

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
        if self.overlays(): tools.append(dict(OVERLAY_TOOL))
        return tools

    def call(self, name: str, args: dict) -> tuple[str, bool]:
        try:
            if name == "knowledge_table": return table_for(self.api, str(args.get("path") or "")), False
            if name == "knowledge_read":  return read_for(self.api, str(args.get("path") or "")), False
            if name == "knowledge_overlay" and self.overlays(): return overlay_call(self.api, args), False
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
            return ok({"prompts": [{"name": "knowledge_start",
                                    "description": "The areas of this domain, and how to search them."}]})
        if method == "prompts/get":
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
