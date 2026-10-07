#!/usr/bin/env python3
"""The walk `check/install-check.sh` runs against the install it just made.

    ./check/install-walk.py <web-port> <circuit-key>

A separate file because it is a different question. The shell script asks whether a clean clone
installs; this asks whether the thing it installed does what the documents say — and it is the half
worth reading when something fails, so it does not live inside a heredoc.

It goes through the **web** port and nothing else: the ontology API is not published outside the
compose network, so anything reachable only from in there is not a path a person or an agent has.
That includes the circuit, which reads this install at the address a person would give another
backbone — and until 2026-10-08 could not, because the surface it reads lived only on 8100.
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

WEB, KEY = int(sys.argv[1]), sys.argv[2]
BASE = f"http://127.0.0.1:{WEB}"
A = f"{BASE}/api/knowledge"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def call(url, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    if data is not None: r.add_header("Content-Type", "application/json")
    r.add_header("X-Knowledge-Actor", "install-check")
    try:
        with urllib.request.urlopen(r, timeout=120) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try: return e.code, json.loads(raw or b"{}")
        except Exception: return e.code, {"error": raw.decode(errors="replace")[:200]}
    except Exception as e: return 0, {"error": type(e).__name__}


def queued(body, wait=0.5):
    """A routing decision, the only way a person can make one: submit, then accept. Both statuses are
    returned — an accept that could not be applied answered 200 once, which is how it went unnoticed."""
    st, p = call(A + "/proposals", "POST", body)
    if st not in (200, 201): return st, p
    st2, d = call(A + f"/proposals/{p['id']}/accept", "POST", {})
    time.sleep(wait)
    return st2, d


class Mcp:
    """Another backbone's agent: an MCP server of its own, opening a circuit to this install."""
    def __init__(self):
        self.p = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"), "--api", A, "--actor", "install-check"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        self.n = 0
        self.rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "install-check", "version": "0"}})
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"); self.p.stdin.flush()
        self.tool("knowledge_table", {})
    def rpc(self, method, params=None):
        self.n += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params or {}}) + "\n"); self.p.stdin.flush()
        return json.loads(self.p.stdout.readline())
    def tool(self, name, args):
        r = self.rpc("tools/call", {"name": name, "arguments": args}).get("result") or {}
        return (r.get("content") or [{}])[0].get("text", "")
    def close(self):
        try: self.p.stdin.close(); self.p.wait(5)
        except Exception: self.p.kill()


# ── the shipped shape ─────────────────────────────────────────────────────────
own = call(A + "/regions")[1].get("regions") or []
check("the worked example is on the map", len(own) == 5, json.dumps([r["source"] for r in own]))
cfg = call(f"{BASE}/api/app-config")[1]
check("the running service says which door it has", cfg.get("auth") == "open", json.dumps(cfg)[:100])
check("  and that the name on a change is a signature", cfg.get("auth_names_the_actor") is False)

st, r = call(A + "/regions", "POST", {
    "source": "site-ops", "representative": {"name": "Site Operations", "id": "site-ops",
                       "one_liner": "Opening, closing, keys, and who to call when something breaks",
                       "use_when": "who opens the office · a key is lost · the lift is stuck"}})
check("a new area can be made", st == 200, json.dumps(r)[:110])

# ── the export decision, through the queue, read by a circuit ────────────────
# One sentence: the line another backbone reads is the area's own `use_when`, edited under scope
# `bb`, and `export` decides whether a circuit sees it at all.
LINE = "who runs the branch site · keys, access, and the on-call for it"
m = Mcp()
opened = m.tool("knowledge_circuit", {"op": "open", "url": BASE, "token": KEY, "name": "here"})
check("another backbone's circuit opens at this install's web address", "CIRCUIT here open" in opened, opened[:200])
read = lambda: m.tool("knowledge_table", {"path": "/v1/circuits/here/regions", "why": "what it shares"})
check("  and sees no area that was not set to export", "/v1/circuits/here/regions/site-ops" not in read(), read()[:200])

st, _ = queued({"scope": "bb", "region": "site-ops", "after": LINE, "why": "what it is chosen by"})
st, d = queued({"scope": "export", "region": "site-ops", "before": "no", "after": "yes", "why": "head office asks"})
t = read()
check("exporting it, through the queue, puts it in the circuit's next read", st == 200 and "/v1/circuits/here/regions/site-ops" in t, f"{st} {t[:300]}")
check("  with the area's own sentence", LINE in t, t[:300])
REVISED = LINE + " · and who holds the spare keys"
st, _ = queued({"scope": "bb", "region": "site-ops", "before": LINE, "after": REVISED, "why": "clearer"})
check("editing the line reaches the reader at once", st == 200 and REVISED in read(), read()[:300])
st, d = queued({"scope": "export", "region": "site-ops", "before": "yes", "after": "no", "why": "stop"})
check("withdrawing it works", st == 200, f"{st} {json.dumps(d)[:150]}")
check("  and the circuit's next read no longer lists it", "/v1/circuits/here/regions/site-ops" not in read(), read()[:300])
m.close()

# `export` is yes or no and both are decisions, so an empty one is a missing field rather than a
# withdrawal.
st, e = call(A + "/proposals", "POST", {"scope": "export", "region": "site-ops", "after": ""})
check("an export decision with nothing in it is refused", st == 422, f"{st} {json.dumps(e)[:120]}")

print("\n".join(results))
print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
