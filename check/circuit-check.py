#!/usr/bin/env python3
"""A circuit into this install, the way another backbone opens one — at the address people use.

    ROUTEMIND_TOKEN=<KNOWLEDGE_CIRCUIT_TOKEN> ./check/circuit-check.py [base]     (base: http://127.0.0.1:8080)

Circuits are the one way left to read another RouteMind (operator, 2026-10-08), and until then the
surface they read lived only on the ontology's own port, which the shipped compose does not publish —
so a circuit could reach an install only where somebody had published 8100 by hand. The web app now
passes `/v1/peers/token` and `/v1/export/…` through, outside its own door. This reads them where a
reader would: through the web port, with nothing but the key.

What must not work is half of it: a wrong key mints nothing, the key itself reads nothing (only a
session does), and the export surface offers no area the owner did not set `export` on.
"""
import json, os, subprocess, sys, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080").rstrip("/")
KEY = os.environ.get("ROUTEMIND_TOKEN", "")
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def call(path, token=None, method="GET"):
    r = urllib.request.Request(BASE + path, data=(b"" if method == "POST" else None), method=method,
                               headers={"X-Peer-Token": token} if token else {})
    try:
        with urllib.request.urlopen(r, timeout=20) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}


if not KEY:
    print("FAIL no key — set ROUTEMIND_TOKEN to this install's KNOWLEDGE_CIRCUIT_TOKEN (check/all.sh reads it from .env)")
    sys.exit(1)

st, _ = call("/v1/peers/token", "not-the-key", "POST")
check("a wrong key mints nothing, through the web port", st == 401, str(st))
st, _ = call("/v1/export/regions", KEY)
check("  and the key itself reads nothing — only a session does", st == 401, str(st))
st, d = call("/v1/peers/token", KEY, "POST")
sess = d.get("token", "")
check("the key mints a six-hour session through the web port", st == 200 and bool(sess) and d.get("expires_in") == 21600, f"{st} {d}")
st, ex = call("/v1/export/regions", sess)
check("  and the session reads the export surface", st == 200 and isinstance(ex.get("regions"), list), f"{st}")

# What crosses is exactly what the owner set `export` on — read from the owner's own view of each area.
st, own = call("/api/knowledge/regions")
exported = set()
for r in own.get("regions", []):
    dir_ = (r.get("fetch") or "").rsplit("/", 1)[-1]
    s2, one = call(f"/api/knowledge/regions/{dir_}")
    if one.get("export"): exported.add(dir_)
crossing = {(r.get("fetch") or "").rsplit("/", 1)[-1] for r in ex.get("regions", [])}
check("  and lists the areas set to export, and only those", crossing <= exported, f"crossing {sorted(crossing)}, exported {sorted(exported)}")

# The whole thing as an agent does it: an MCP server pointed at nothing in particular opens a circuit
# to this install's address and walks it.
m = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"), "--api", f"{BASE}/api/knowledge", "--actor", "circuit-check"],
                     env={**os.environ, "KNOWLEDGE_WALK_CHECK": "1"},   # its walks are a check's, not an agent's
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
n = [0]
def rpc(method, params=None):
    n[0] += 1; m.stdin.write(json.dumps({"jsonrpc": "2.0", "id": n[0], "method": method, "params": params or {}}) + "\n"); m.stdin.flush()
    return json.loads(m.stdout.readline())
def tool(name, args):
    r = rpc("tools/call", {"name": name, "arguments": args}).get("result") or {}
    return (r.get("content") or [{}])[0].get("text", ""), bool(r.get("isError"))
rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "circuit-check", "version": "0"}})
m.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"); m.stdin.flush()
tool("knowledge_table", {})
t, err = tool("knowledge_circuit", {"op": "open", "url": BASE, "token": KEY, "name": "self"})
check("an agent's circuit opens at the install's address", not err and "CIRCUIT self open" in t, t[:200])
t, err = tool("knowledge_table", {"path": "/v1/circuits/self/regions", "why": "what this install shares"})
check("  and reads what it shares, under the circuit's own addresses",
      not err and all(f"/v1/circuits/self/regions/{a}" in t for a in crossing), t[:300])
if crossing:
    a = sorted(crossing)[0]
    t, err = tool("knowledge_table", {"path": f"/v1/circuits/self/regions/{a}", "why": "inside one area"})
    check(f"  and walks into {a}", not err and "/v1/circuits/self/" in t, t[:200])
else:
    results.append("--   no area here is set to export, so the walk into one was not tried")
m.stdin.close(); m.wait(5)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
