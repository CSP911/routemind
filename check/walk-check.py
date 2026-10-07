#!/usr/bin/env python3
"""Invariant 1 at the agent's door: every walk starts at hop 0 — and the agent carries nothing to prove it.

    ./check/walk-check.py [port]

Starts an ontology on a copy of the shipped repository and drives the MCP server over stdio the way
an agent does. The server remembers, for the session it serves, whether hop 0 has been opened: below
hop 0 a table or a document is refused until it has, and every step needs a one-line reason. No id is
handed to the agent (operator, 2026-10-07) — so the thing to check is that the refusal still fires on
every path below hop 0 without one, that it says how to start, that it expires, and that the agent is
shown four tools and no more.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18190
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


class Mcp:
    def __init__(self, env=None):
        self.p = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"),
                                   "--api", f"http://127.0.0.1:{PORT}/v1", "--actor", "walk-check"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                                  env={**os.environ, **(env or {})})
        self.n = 0
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "walk-check", "version": "0"}}})
        self._recv()
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    def _id(self): self.n += 1; return self.n
    def _send(self, m): self.p.stdin.write(json.dumps(m) + "\n"); self.p.stdin.flush()
    def _recv(self): return json.loads(self.p.stdout.readline())
    def tools(self):
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "tools/list", "params": {}})
        return self._recv()["result"]["tools"]
    def call(self, name, args):
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "tools/call", "params": {"name": name, "arguments": args}})
        r = self._recv().get("result") or {}
        return (r.get("content") or [{}])[0].get("text", ""), bool(r.get("isError"))
    def close(self):
        try: self.p.stdin.close(); self.p.wait(5)
        except Exception: self.p.kill()


T = tempfile.mkdtemp(prefix="walk-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, symlinks=True)
subprocess.run(["git", "-C", repo, "config", "user.email", "walk@routemind"], check=True)
subprocess.run(["git", "-C", repo, "config", "user.name", "walk-check"], check=True)
os.makedirs(os.path.join(T, "overlays"), exist_ok=True)
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_OVERLAYS": os.path.join(T, "overlays"),
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                       stdout=open(os.path.join(T, "svc.log"), "w"), stderr=subprocess.STDOUT)
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else:
    svc.kill(); sys.exit("  the ontology never answered — log:\n" + open(os.path.join(T, "svc.log")).read()[-1500:])

try:
    m = Mcp()
    tools = m.tools()
    names = [t["name"] for t in tools]
    check("the agent is shown four tools: table, read, place, circuit", names == ["knowledge_table", "knowledge_read", "knowledge_place", "knowledge_circuit"], str(names))
    check("  overlay stays off although this backbone keeps overlays", "knowledge_overlay" not in names)
    props = {t["name"]: set((t.get("inputSchema") or {}).get("properties", {})) for t in tools}
    check("  and no tool asks the agent for a walk id", not any("walk" in p for p in props.values()), json.dumps({k: sorted(v) for k, v in props.items()}))
    check("  the first tool's description carries hop 0", "/v1/regions/expense" in tools[0]["description"])

    # ── below hop 0, before hop 0 ────────────────────────────────────────────
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense", "why": "receipts"})
    check("an area's table before hop 0 is refused", err and "hop 0" in t, t[:140])
    check("  and the refusal says how to start: knowledge_table with no address", "knowledge_table with no address" in t, t[:200])
    t, err = m.call("knowledge_read", {"path": "/v1/nodes/qualified-list/body", "why": "the list"})
    check("a document before hop 0 is refused", err and "hop 0" in t, t[:140])

    # ── hop 0, then below it ─────────────────────────────────────────────────
    t, err = m.call("knowledge_table", {})
    check("hop 0 with no address answers", not err and "/v1/regions/expense" in t, t[:120])
    check("  and prints no id for the agent to carry", "wk_" not in t and "walk  " not in t, t[:160])
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense"})
    check("below hop 0 a step without a reason is refused", err and "why" in t, t[:140])
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense", "why": "receipts are in its sentence"})
    check("  with a reason the area's table opens", not err and "/v1/nodes/" in t, t[:140])
    t, err = m.call("knowledge_read", {"path": "/v1/nodes/qualified-list/body", "why": "the evidence list"})
    check("  and a document opens", not err and "Qualifying evidence" in t, t[:140])
    m.call("knowledge_table", {})
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense", "why": "again"})
    check("a new hop 0 starts the next walk and the agent goes on without any argument", not err, t[:140])

    t, err = m.call("knowledge_place", {"op": "open", "name": "Pigeon loft rota", "one_liner": "Who feeds the pigeons"})
    check("placement is its own walk and needs no hop 0 of this kind", not err and "/v1/regions/expense" in t, t[:160])
    m.call("knowledge_place", {"op": "close", "id": "p1"})
    m.close()

    # ── it expires ───────────────────────────────────────────────────────────
    m2 = Mcp(env={"KNOWLEDGE_WALK_TTL": "1"})
    m2.call("knowledge_table", {}); time.sleep(1.5)
    t, err = m2.call("knowledge_table", {"path": "/v1/regions/expense", "why": "late"})
    check("a walk expires, and the refusal says how to start again", err and "expired" in t and "knowledge_table with no address" in t, t[:200])
    m2.close()

    # ── the switch ───────────────────────────────────────────────────────────
    m3 = Mcp(env={"KNOWLEDGE_TOOLS_EXTRA": "overlay"})
    check("KNOWLEDGE_TOOLS_EXTRA=overlay turns the overlay tool back on", "knowledge_overlay" in [t["name"] for t in m3.tools()])
    m3.close()
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
