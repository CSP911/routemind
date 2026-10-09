#!/usr/bin/env python3
"""Placing a document by walking the table — through the MCP, the way an agent does it.

    ./check/place-check.py

Starts an ontology on a copy of the shipped corpus and drives `knowledge_place` over stdio: open,
read hop 0, step into an area, `here` — then reads back what was written. A pick the table did not
print is refused; `none` at hop 0 writes nothing and asks for an area.

What the tables carry is each row's line and nothing else. Until 2026-10-07 every row also carried
the words it shared with the document, and `here` queued proposals to widen the lines above by a
string-matching rule. Both are gone, and the half of this file that tested them with them; what is
checked instead is that neither comes back — no shared-word column, no proposal queued by a placement.

Since 2026-10-09 `here` is a change set (docs/CHANGE.md): the line over the document has to be
decided — kept or reworded — or nothing is written, and the refusal prints the line. The set itself
is check/change-check.py's; here it is the walk around it.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


# ── the whole walk, through the MCP, on a copy of the shipped corpus ───────────
PORT = int(os.environ.get("PLACE_CHECK_PORT") or 18120)
tmp = tempfile.mkdtemp(prefix="place-check-")
repo = os.path.join(tmp, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, symlinks=True)
subprocess.run(["git", "-C", repo, "config", "user.email", "check@routemind"], check=True)
subprocess.run(["git", "-C", repo, "config", "user.name", "place-check"], check=True)
# The proposal queue lives in the harness store; without it the queue answers 501 and `here` can
# place but not advertise. The check needs both halves, so it gives the server one.
os.makedirs(os.path.join(tmp, "harness"), exist_ok=True)
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_HARNESS": os.path.join(tmp, "harness"),
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                       stdout=open(os.path.join(tmp, "svc.log"), "w"), stderr=subprocess.STDOUT)


def _end():
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(tmp, ignore_errors=True)


def _log_tail():
    try:
        with open(os.path.join(tmp, "svc.log"), encoding="utf-8", errors="replace") as f:
            return "".join(f.readlines()[-25:])
    except Exception: return "(no server log)"


import atexit; atexit.register(_end)
for _ in range(80):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else:
    # A server that never answered is the one failure the rest of this file cannot explain, and
    # its log is in a directory that is about to be removed. Print it before anything else fails.
    print("\n".join(results)); print(f"\nFAIL the ontology never answered on :{PORT} — its log:\n{_log_tail()}"); sys.exit(1)


def get(path):
    """A read, or the status it refused with — never an exception. A refused read should fail the
    assertion that needed it, with the code in the message, rather than end the run unexplained."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=20) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code} from {path}"}


# Whatever ends this run early, the assertions that already ran are the evidence; print them.
atexit.register(lambda: print("\n".join(results)) if results and not getattr(sys, "_place_check_done", False) else None)


class Mcp:
    """One MCP process over stdio, one call at a time."""
    def __init__(self):
        self.p = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"),
                                   "--api", f"http://127.0.0.1:{PORT}/v1", "--actor", "place-check"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        self.n = 0
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "place-check", "version": "0"}}})
        self._recv()
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    def _id(self): self.n += 1; return self.n
    def _send(self, m): self.p.stdin.write(json.dumps(m) + "\n"); self.p.stdin.flush()
    def _recv(self): return json.loads(self.p.stdout.readline())
    def call(self, name, args):
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "tools/call", "params": {"name": name, "arguments": args}})
        m = self._recv()
        r = m.get("result") or {}
        return (r.get("content") or [{}])[0].get("text", ""), bool(r.get("isError"))
    def close(self):
        try: self.p.stdin.close(); self.p.wait(5)
        except Exception: self.p.kill()


m = Mcp()
atexit.register(m.close)
tools_text, _ = m.call("knowledge_place", {"op": "list"})
check("the tool answers", "No placement is open" in tools_text, tools_text[:80])

DOC = {"name": "Overseas vendor registration", "one_liner": "How to register a vendor based abroad with no Korean business number"}
text, err = m.call("knowledge_place", {"op": "open", "name": DOC["name"], "one_liner": DOC["one_liner"],
                                       "content": "# Overseas vendor registration\n\nWritten 1 October 2026.\n"})
check("open prints hop 0", not err and "/v1/regions/procurement" in text and "/v1/regions/expense" in text, text[:200])
pid = text.split("[", 1)[1].split("]", 1)[0] if "[" in text else ""
check("  with a placement id", pid.startswith("p"), pid)
proc = next(r for r in get("/v1/regions")["regions"] if r["source"] == "procurement")
row = next((l for l in text.splitlines() if "/v1/regions/procurement" in l), "")
check("  each row is its address and its line", proc["use_when"][:60] in row, row)
check("  and nothing else — no column of shared words", "SHARES" not in text and "terms" not in text, text[:300])

text, err = m.call("knowledge_place", {"op": "step", "id": pid, "pick": "/v1/regions/payroll/../procurement"})
check("a pick the table did not print is refused", err and "not an address the last table printed" in text, text[:120])
text, err = m.call("knowledge_place", {"op": "here", "id": pid})
check("`here` at hop 0 is refused", err and "hop 0" in text, text[:120])

text, err = m.call("knowledge_place", {"op": "step", "id": pid, "pick": "/v1/regions/procurement"})
check("step into procurement prints its table", not err and "child of procurement in procurement" in text, text[:300])
addrs = [l.split()[0] for l in text.splitlines() if l.strip().startswith("/v1/nodes/")]
check("  with node addresses to descend into", len(addrs) > 0, str(addrs[:5]))

before = {q["id"] for q in get("/v1/curator/proposals").get("proposals") or []}
line_before = proc["use_when"]
text, err = m.call("knowledge_place", {"op": "here", "id": pid, "why": "the check places one"})
check("`here` with the line over it undecided writes nothing, and says which line", not err and text.startswith("NOT WRITTEN")
      and "procurement.use_when: UNDECIDED" in text, text[:200])
text, err = m.call("knowledge_place", {"op": "here", "id": pid, "why": "the check places one",
                                       "decisions": [{"op": "keep", "id": "procurement", "field": "use_when", "why": "its sentence covers it"}]})
check("`here` with the line kept places it", not err and text.startswith("PLACED"), text[:200])
nid = text.split(" as ", 1)[1].split(" — ", 1)[0].strip() if " as " in text else ""
node = get(f"/v1/nodes/{nid}") if nid else {}
check("  the node exists afterwards", bool(node.get("id")), str(node)[:120])
check("  under the parent the walk reached", node.get("parent") == "procurement", f"parent={node.get('parent')!r}")
check("  the walk is on record", "walked  :" in text and "/v1/regions/procurement" in text)
after = {q["id"] for q in get("/v1/curator/proposals").get("proposals") or []}
check("  no proposal was queued by the placement", after == before, str(sorted(after - before)))
check("  and the area's sentence is unchanged",
      next(r for r in get("/v1/regions")["regions"] if r["source"] == "procurement")["use_when"] == line_before)
check("  and says the line over it was kept", "procurement.use_when keep" in text, text[-200:])
check("  and the placement is closed", "No placement is open" in m.call("knowledge_place", {"op": "list"})[0])

# `none` at hop 0: nothing written, an area asked for.
text, err = m.call("knowledge_place", {"op": "open", "name": "Pigeon loft rota", "one_liner": "Who feeds the pigeons on which day"})
pid = text.split("[", 1)[1].split("]", 1)[0]
n_before = len(get("/v1/nodes")["nodes"])
text, err = m.call("knowledge_place", {"op": "step", "id": pid, "pick": "none"})
check("`none` at hop 0 asks for a new area and writes nothing",
      not err and "new area" in text and "Nothing was written" in text and len(get("/v1/nodes")["nodes"]) == n_before, text[:200])
check("  and offers to make it with `here` and `area`, in the document's commit", "area:" in text and "here {" in text, text[:300])
check("  offering the document's own line as the sentence", "Who feeds the pigeons" in text)

sys._place_check_done = True
print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
