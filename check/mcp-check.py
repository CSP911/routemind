#!/usr/bin/env python3
"""Drive the MCP server the way a client does — over stdio, one JSON object per line.

    ./check/mcp-check.py [api-url]

Checks the protocol (an agent that cannot initialise sees no tools at all), and then the thing that
actually matters: that an agent handed nothing but these two tools can find a document. So the last
part walks the ontology the way an agent would — areas, then one area, then read what it points at —
using only addresses the tables printed.
"""
import atexit, json, os, subprocess, sys, traceback

API = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080/api/knowledge"
HERE = os.path.dirname(os.path.abspath(__file__))
results = []


def check(name, cond):
    results.append(("ok  " if cond else "FAIL") + " " + name)
    return cond


# Results are printed however this ends. A desynchronised stream makes the *next* read return the
# wrong object, so the failure surfaces as a KeyError three steps later — and a check that dies
# instead of reporting looks, to anyone reading the output, exactly like a check that never ran.
@atexit.register
def _report():
    if results: print("\n".join(results))


sys.excepthook = lambda k, v, t: (results.append(
    "FAIL the check crashed (a desynchronised stream shows up like this): "
    + "".join(traceback.format_exception_only(k, v)).strip()), sys.stderr.write("".join(traceback.format_exception(k, v, t))))


class Client:
    def __init__(self):
        self.p = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "..", "mcp", "knowledge_mcp.py"), "--api", API],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        self.n = 0

    def call(self, method, params=None, notify=False):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None: msg["params"] = params
        if not notify:
            self.n += 1; msg["id"] = self.n
        self.p.stdin.write(json.dumps(msg) + "\n"); self.p.stdin.flush()
        if notify: return None
        line = self.p.stdout.readline()
        return json.loads(line) if line else None

    def text(self, tool, args=None):
        r = self.call("tools/call", {"name": tool, "arguments": args or {}})
        c = (r.get("result") or {}).get("content") or [{}]
        return c[0].get("text", ""), bool((r.get("result") or {}).get("isError"))

    def close(self):
        self.p.stdin.close(); self.p.terminate()


c = Client()
init = c.call("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                             "clientInfo": {"name": "check", "version": "0"}})
check("initialize answers", bool(init and "result" in init))
check("it echoes the protocol version the client asked for",
      (init["result"] or {}).get("protocolVersion") == "2024-11-05")
check("it declares tools", "tools" in (init["result"].get("capabilities") or {}))

# The server instructions carry the areas, because a client that loads MCP tools lazily — Claude Code
# does — shows the model two tool NAMES and nothing else until it decides to look. Measured: asked a
# domain question without being told to use Knowledge, it grepped the repository and answered from
# general knowledge. With the areas in the instructions, the same question in the same session went
# straight to the right area. The instructions are what tells a model a question belongs here at all.
instr = (init["result"] or {}).get("instructions") or ""
check("initialize carries instructions", bool(instr.strip()))
check("they name the areas, so a model can tell a question belongs here", "/v1/regions/" in instr)
check("they say to consult it before answering generically", "BEFORE" in instr)

# A notification has no id and must produce no reply. A server that answers one desynchronises the
# stream, and every response after it belongs to the wrong request.
c.call("notifications/initialized", {}, notify=True)
pong = c.call("ping")
check("a notification is not answered", pong is not None and pong.get("id") == c.n)

tools = c.call("tools/list")["result"]["tools"]
names = [t["name"] for t in tools]
# Two tools for the two things an agent does, and a third — the working set — only where this install
# keeps overlays. Asserted in whichever direction the install is, so neither case passes vacuously.
import urllib.request, urllib.error
try:
    urllib.request.urlopen(API.rstrip("/") + "/overlays?state=open", timeout=10); has_overlays = True
except urllib.error.HTTPError:
    has_overlays = False
want = ["knowledge_table", "knowledge_read"] + (["knowledge_overlay"] if has_overlays else [])
check(f"{len(want)} tools — the two an agent walks with{', and the overlay' if has_overlays else ''}", names == want)

# The areas have to reach the model before it decides anything, and a tool description is the only
# text every MCP client shows it.
desc = tools[0]["description"]
check("the area list rides in the tool description", "ADDRESS" in desc and "/v1/regions" in desc)
check("absence is claimed only for the whole list", "grounds on which you may say" in desc)

# Walk it as an agent would: nothing but addresses the tables printed.
top, err = c.text("knowledge_table")
check("no arguments gives the areas", not err and "/v1/regions/" in top)

addrs = [w for line in top.splitlines() for w in line.split() if w.startswith("/v1/regions/")]
check("the area list printed at least one address", bool(addrs))
if addrs:
    area, err = c.text("knowledge_table", {"path": addrs[0]})
    check(f"the area table fetches ({addrs[0]})", not err)
    check("an area does not claim absence for the world", "go back to /v1/regions" in area)
    # A document address taken out of the rendered table, because the text is all an agent has. It
    # matched `/files/` until 2026-09-11, which no table has printed since flattening gave a body its
    # own address — `/v1/nodes/<id>/body`, and `/files/` disappeared (mcp/knowledge_mcp.py). So it
    # skipped on every install and said so as "this area holds no document yet", which reads as a gap
    # in someone's ontology rather than a check aimed at an address shape that no longer exists.
    # Reading the KIND column instead ties it to the contract the table states — `file` is the row
    # `knowledge_read` takes — rather than to the spelling of a path.
    files = [p[1] for line in area.splitlines() if (p := line.split())[:1] == ["file"] and len(p) > 1]
    if files:
        doc, err = c.text("knowledge_read", {"path": files[0]})
        check(f"the document reads ({files[0]})", not err and len(doc) > 0)
    else:
        results.append("--   that area holds no document yet; the read step needs one")

# Three states, three answers. `empty` is the one easy to get wrong in both directions: call it a
# table and an agent spends a hop finding nothing; call it a document and `knowledge_read` 404s.
import urllib.request
entries = []
if addrs:
    with urllib.request.urlopen(API + "/regions/" + addrs[0].rsplit("/", 1)[1]) as r:
        entries = (json.load(r).get("entries") or [])
kinds = {e.get("type") for e in entries}
if "data" in kinds:
    row = next(e for e in entries if e.get("type") == "data")
    doc, err = c.text("knowledge_read", {"path": row["fetch"]})
    check("a data row's own address reads as a document", not err and len(doc) > 0)
else:
    results.append("--   no written document here; that row of the table is unchecked")
if "empty" in kinds:
    row = next(e for e in entries if e.get("type") == "empty")
    line = next((l for l in area.splitlines() if row["fetch"] in l), "")
    check("an empty row is labelled empty, not table", line.strip().startswith("empty"))
    _, err = c.text("knowledge_read", {"path": row["fetch"] + "/body"})
    check("and reading it says nobody wrote it", err)
else:
    results.append("--   no empty entity here; that row of the table is unchecked")

# Refusals have to say what to do instead, not just fail.
bad, err = c.text("knowledge_read", {"path": "/v1/regions"})
check("reading a table says to call the other tool", err and "knowledge_table" in bad)
bad, err = c.text("knowledge_table", {"path": "regions/made-up"})
check("an invented address is refused with the shapes that work", err and "/v1/regions/<area>" in bad)

c.close()
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
