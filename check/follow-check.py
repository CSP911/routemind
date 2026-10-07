#!/usr/bin/env python3
"""Invariant 3, the derived state that is not a file: what a reader holds follows its source.

    ./check/follow-check.py [port]

`regions.json` has its own check (drift-check). This is the rest of the inventory in
docs/INVARIANTS.md — state a running backbone or its agent keeps that is derived from something else,
and the one question for each: when the source changes, does this follow, now, without anybody
waiting out a timer?

  what a circuit reads     source: the other backbone's export surface. Nothing is cached — every
                           read through a circuit is a read of the far end — so an area exported or
                           withdrawn there is in or out of the next table here.
  a circuit's session      source: the far end's memory. A restart there revokes every session; the
                           circuit must re-mint on the 401 and carry on, not fail the walk.
  the MCP's area list      source: hop 0. It is written into the first tool's description, refreshed
                           on every tools/list — an area created after the client connected must be
                           in the next listing without a restart.

Two backbones: ay, which the MCP serves, and bee, which a circuit from that MCP reads. (Until
2026-10-08 this also followed a standing link's cached advertisement and a session's `peers.yaml`;
both went with standing links.)
"""
import json, os, re, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18230
PORT_B = PORT + 1
TOKEN_A, TOKEN_B = "follow-check-key-for-ay", "follow-check-key-for-bee"
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def req(port, method, path, body=None, token=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, method=method,
                               headers={"Content-Type": "application/json", "X-Knowledge-Actor": "follow-check", **({"X-Peer-Token": token} if token else {})})
    try:
        with urllib.request.urlopen(r, timeout=30) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}
    except Exception as e: return 0, {"error": type(e).__name__}


def session(port, key):
    st, d = req(port, "POST", "/v1/peers/token", token=key); return d.get("token", "")


def git(repo, *a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout.strip()


def start(repo, port, own_token, extra):
    env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(port), "ONTOLOGY_PEER_TOKEN": own_token,
           **extra,
           "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
    for k in [k for k in env if k.startswith("ONTOLOGY_LLM_")]: env.pop(k)
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                         stdout=open(os.path.join(repo, "..", f"svc-{port}.log"), "a"), stderr=subprocess.STDOUT)
    procs.append(p)
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); return p
        except Exception: time.sleep(0.25)
    sys.exit(f"  the backbone on {port} did not start — " + open(os.path.join(repo, "..", f"svc-{port}.log")).read()[-800:])


def stop(p):
    p.terminate()
    try: p.wait(5)
    except Exception: p.kill()


def within(seconds, cond):
    end = time.time() + seconds
    while time.time() < end:
        if cond(): return True
        time.sleep(0.25)
    return cond()


T = tempfile.mkdtemp(prefix="follow-check-")
repo_a, repo_b = os.path.join(T, "ay"), os.path.join(T, "bee")
for repo in (repo_a, repo_b):
    shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
    git(repo, "init", "-q"); git(repo, "config", "user.email", "f@r"); git(repo, "config", "user.name", "follow")
for repo in (repo_a, repo_b): git(repo, "add", "-A"); git(repo, "commit", "-qm", "as shipped")
# bee's first area, so that exporting and withdrawing it are both visible through the circuit
area_b = sorted(d for d in os.listdir(os.path.join(repo_b, "regions")) if os.path.isdir(os.path.join(repo_b, "regions", d)))[0]

try:
    a = start(repo_a, PORT, TOKEN_A, {})
    b = start(repo_b, PORT_B, TOKEN_B, {})
    # nothing exported on bee to begin with, whatever the copied data says
    st, rows = req(PORT_B, "GET", "/v1/regions")
    for r in rows.get("regions", []):
        rep = r.get("representative")
        if rep: req(PORT_B, "PUT", f"/v1/nodes/{rep}", {"export": "no"})

    m = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"), "--api", f"http://127.0.0.1:{PORT}/v1", "--actor", "follow-check"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    n = [0]
    def rpc(method, params=None):
        n[0] += 1; m.stdin.write(json.dumps({"jsonrpc": "2.0", "id": n[0], "method": method, "params": params or {}}) + "\n"); m.stdin.flush()
        return json.loads(m.stdout.readline())
    def tool(name, args):
        r = rpc("tools/call", {"name": name, "arguments": args}).get("result") or {}
        return (r.get("content") or [{}])[0].get("text", ""), bool(r.get("isError"))
    rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "follow-check", "version": "0"}})
    m.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"); m.stdin.flush()
    tool("knowledge_table", {})                                   # hop 0, so the walk may go below it

    # ── what a circuit reads follows the far end ──────────────────────────────
    t, err = tool("knowledge_circuit", {"op": "open", "url": f"http://127.0.0.1:{PORT_B}", "token": TOKEN_B, "name": "bee"})
    check("a circuit to bee opens", not err and "CIRCUIT bee open" in t, t[:160])
    circuit = lambda: tool("knowledge_table", {"path": "/v1/circuits/bee/regions", "why": "what bee shares"})[0]
    check("  and with nothing exported there, it lists nothing", f"/v1/circuits/bee/regions/{area_b}" not in circuit(), circuit()[:200])
    req(PORT_B, "PUT", f"/v1/nodes/{area_b}", {"export": "yes"})
    check("bee exports an area: the next read through the circuit lists it", f"/v1/circuits/bee/regions/{area_b}" in circuit(), circuit()[:300])
    NEW = "what a partner may ask here · the line bee changed"
    req(PORT_B, "PUT", f"/v1/nodes/{area_b}", {"use_when": NEW})
    check("bee rewrites its line: the next read carries the new one", NEW in circuit(), circuit()[:300])
    req(PORT_B, "PUT", f"/v1/nodes/{area_b}", {"export": "no"})
    check("bee withdraws it: the next read no longer lists it", f"/v1/circuits/bee/regions/{area_b}" not in circuit(), circuit()[:300])

    # ── a circuit's session survives the far end restarting ───────────────────
    req(PORT_B, "PUT", f"/v1/nodes/{area_b}", {"export": "yes"})
    stop(b); b = start(repo_b, PORT_B, TOKEN_B, {})              # every session bee had is gone
    t = circuit()
    check("bee restarts, revoking every session: the circuit re-mints and reads on", f"/v1/circuits/bee/regions/{area_b}" in t, t[:300])
    st, d = req(PORT_B, "GET", "/v1/export/regions", token=TOKEN_B)
    check("  while the enrolment key itself still reads nothing — only a session does", st == 401, f"{st}")

    # ── the MCP's area list follows hop 0 ─────────────────────────────────────
    desc = lambda: rpc("tools/list")["result"]["tools"][0]["description"]
    check("the first tool's description carries hop 0", "/v1/regions/" in desc())
    check("  and not an area that does not exist yet", "/v1/regions/follow-area" not in desc())
    st, d = req(PORT, "POST", "/v1/regions", {"source": "follow-area", "representative": {"id": "follow-area", "name": "Follow Area", "one_liner": "x", "use_when": "when the check adds an area"}})
    check("an area is created on ay while the MCP is connected", 200 <= st < 300, f"{st}")
    check("  and the next tools/list carries it, without a restart", "/v1/regions/follow-area" in desc(), desc()[-300:])
    m.stdin.close(); m.wait(5)
finally:
    for p in procs: stop(p)
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
