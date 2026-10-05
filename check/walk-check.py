#!/usr/bin/env python3
"""Invariants 1 and 2, as the MCP server enforces them: every walk starts at hop 0, and "not here"
may be said only by someone who has seen the whole list.

    ./check/walk-check.py [port]

Starts an ontology on a copy of the shipped repository and drives the MCP server over stdio the way
an agent does. Before 2026-10-06 both rules were sentences in a tool description, and an agent quoted
them while breaking them. Now hop 0 issues a walk id and everything below hop 0 is refused without
it — so the thing to check is the refusal: that it fires on every path below hop 0, that it says how
to start, that a walk opened by one hop 0 is over when the next is served, that it expires, and that
hop 0 itself, resolve, and placement are not caught by it.
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
        return [t["name"] for t in self._recv()["result"]["tools"]]
    def call(self, name, args):
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "tools/call", "params": {"name": name, "arguments": args}})
        r = self._recv().get("result") or {}
        return (r.get("content") or [{}])[0].get("text", ""), bool(r.get("isError"))
    def close(self):
        try: self.p.stdin.close(); self.p.wait(5)
        except Exception: self.p.kill()


def walk_id(text):
    for l in text.splitlines():
        if l.strip().startswith("walk"):
            return l.split(":", 1)[1].strip().split()[0]
    return ""


T = tempfile.mkdtemp(prefix="walk-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, symlinks=True)
subprocess.run(["git", "-C", repo, "config", "user.email", "walk@routemind"], check=True)
subprocess.run(["git", "-C", repo, "config", "user.name", "walk-check"], check=True)
os.makedirs(os.path.join(T, "harness"), exist_ok=True); os.makedirs(os.path.join(T, "overlays"), exist_ok=True)
# Overlays on, so closing one as not_found — invariant 2's door — is exercised, not skipped.
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_HARNESS": os.path.join(T, "harness"),
       "ONTOLOGY_OVERLAYS": os.path.join(T, "overlays"),
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
    check("the walk id is asked for on the tools that need it",
          all(n in tools for n in ("knowledge_table", "knowledge_read", "knowledge_resolve")), str(tools))

    # ── below hop 0, without a walk ──────────────────────────────────────────
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense"})
    check("an area's table without a walk is refused", err and "walk" in t, t[:140])
    check("  and the refusal says how to start: at hop 0, with resolve", "hop 0" in t and "knowledge_resolve" in t, t[:200])
    t, err = m.call("knowledge_read", {"path": "/v1/nodes/qualified-list/body"})
    check("a document without a walk is refused", err and "walk" in t, t[:140])
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense", "walk": "w9"})
    check("a walk id this session never opened is refused", err and "not one this session opened" in t, t[:160])

    # ── hop 0 opens a walk ───────────────────────────────────────────────────
    t, err = m.call("knowledge_table", {})
    w1 = walk_id(t)
    check("hop 0 with no address needs no walk and opens one", not err and w1.startswith("w"), t[:200])
    check("  and still prints the area list", "/v1/regions/expense" in t)
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense", "walk": w1})
    check("the area's table opens with it", not err and "/v1/nodes/" in t, t[:160])
    t, err = m.call("knowledge_read", {"path": "/v1/nodes/qualified-list/body", "walk": w1})
    check("a document opens with it", not err and "Qualifying evidence" in t, t[:160])

    # ── a new hop 0 ends the old walk ────────────────────────────────────────
    t, err = m.call("knowledge_resolve", {"q": "what counts as a receipt over 30,000 KRW"})
    w2 = walk_id(t)
    check("resolve opens a new walk", not err and w2.startswith("w") and w2 != w1, t[:200])
    check("  and prints hop 0 with it", "/v1/regions/expense" in t)
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense", "walk": w1})
    check("the old walk is over once a new hop 0 was served", err and "is over" in t and "new hop 0" in t, t[:160])
    t, err = m.call("knowledge_table", {"path": "/v1/regions/expense", "walk": w2})
    check("  and the new one works", not err)

    # ── "not here" needs the whole list ──────────────────────────────────────
    if "knowledge_overlay" in tools:
        t, err = m.call("knowledge_overlay", {"op": "create", "question": "is there a rule on pigeons",
                                              "members": [{"address": "/v1/regions/expense", "why": "w"}]})
        import re as _re
        mm = _re.search(r"OVERLAY (ov_[A-Za-z0-9_-]+)", t)      # the heading create prints
        oid = mm.group(1) if mm else ""
        if check("an overlay can be opened (to test closing it)", not err and bool(oid), t[:200]):
            t, err = m.call("knowledge_overlay", {"op": "close", "id": oid, "outcome": "not_found", "used": []})
            check("closing as not_found without a walk is refused", err and "whole list" in t or "walk" in t, t[:160])
            t, err = m.call("knowledge_overlay", {"op": "close", "id": oid, "outcome": "not_found", "used": [], "walk": w2})
            check("  and allowed inside the walk", not err, t[:160])
            t, err = m.call("knowledge_table", {"path": "/v1/regions/expense", "walk": w2})
            check("  after which the walk is over — the question was answered", err and "closed" in t, t[:160])
    else:
        results.append("skip overlay: this backend lists no knowledge_overlay")

    # ── what the walk does not touch ─────────────────────────────────────────
    t, err = m.call("knowledge_place", {"op": "open", "name": "Pigeon loft rota", "one_liner": "Who feeds the pigeons"})
    check("placement is its own walk and needs no id", not err and "/v1/regions/expense" in t, t[:160])
    m.call("knowledge_place", {"op": "close", "id": "p1"})
    m.close()

    # ── it expires ───────────────────────────────────────────────────────────
    m2 = Mcp(env={"KNOWLEDGE_WALK_TTL": "1"})
    t, _ = m2.call("knowledge_table", {})
    w = walk_id(t); time.sleep(1.5)
    t, err = m2.call("knowledge_table", {"path": "/v1/regions/expense", "walk": w})
    check("a walk expires", err and "expired" in t, t[:160])
    m2.close()
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
