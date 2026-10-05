#!/usr/bin/env python3
"""Invariant 3, the derived state that is not a file: caches and sessions follow their source.

    ./check/follow-check.py [port]

`regions.json` has its own check (drift-check). This is the rest of the inventory in
docs/INVARIANTS.md — every piece of state a running backbone keeps that is derived from something
else, and the one question for each: when the source changes, does this follow, now, without
anybody waiting out a timer?

  a peer's advertisement   source: the peer's export surface. Cached five seconds (ADVERT_TTL), and
                           the peer pokes `/v1/export/refresh` when its export state changes. With
                           the cache set to sixty seconds here, only the poke can carry a change —
                           so a change that arrives within three seconds arrived by the poke, and a
                           control run with no back-link shows it would not have arrived otherwise.
  a reader's session       source: peers.yaml. A session says who the caller was when it was minted;
                           `sessions_follow` drops every session when the declared peers change.
                           Removing the peer from the file, by hand and committed, must end its
                           session on the very next read.
  the MCP's area list      source: hop 0. It is written into the first tool's description, refreshed
                           on every tools/list — an area created after the client connected must be
                           in the next listing without a restart.

Two backbones, ay and bee, linked both ways as the peering check links them; the MCP against ay.
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


def link(repo, name, port, token_env):
    open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
        f"peers:\n  - name: {name}\n    label: {name.upper()}\n    url: http://127.0.0.1:{port}\n    token_env: {token_env}\n")


def start(repo, port, own_token, extra):
    env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(port), "ONTOLOGY_PEER_TOKEN": own_token,
           "PEERTOK_A": TOKEN_A, "PEERTOK_B": TOKEN_B, **extra,
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


def peer_rows(port):
    st, d = req(port, "GET", "/v1/regions")
    return {r.get("source"): r for r in d.get("regions", []) if r.get("peer")}


T = tempfile.mkdtemp(prefix="follow-check-")
repo_a, repo_b = os.path.join(T, "ay"), os.path.join(T, "bee")
for repo in (repo_a, repo_b):
    shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
    git(repo, "init", "-q"); git(repo, "config", "user.email", "f@r"); git(repo, "config", "user.name", "follow")
link(repo_a, "bee", PORT_B, "PEERTOK_B"); link(repo_b, "ay", PORT, "PEERTOK_A")
for repo in (repo_a, repo_b): git(repo, "add", "-A"); git(repo, "commit", "-qm", "linked")
# bee's first area, so that withdrawing and advertising it are both visible from ay
area_b = sorted(d for d in os.listdir(os.path.join(repo_b, "regions")) if os.path.isdir(os.path.join(repo_b, "regions", d)))[0]
src_b = area_b.replace("-", "_")

try:
    a = start(repo_a, PORT, TOKEN_A, {"ONTOLOGY_PEER_TTL": "60"})      # only a poke can refresh ay inside a minute
    b = start(repo_b, PORT_B, TOKEN_B, {})

    # ── a peer's advertisement follows the peer ───────────────────────────────
    check("ay sees no area of bee's yet (nothing exported)", src_b not in peer_rows(PORT), str(list(peer_rows(PORT))))
    st, d = req(PORT_B, "PUT", f"/v1/nodes/{area_b}", {"export": "yes"})
    check("bee exports an area (a write on bee)", 200 <= st < 300, f"{st} {json.dumps(d)[:100]}")
    arrived = check("  and ay lists it within three seconds — the poke, not the sixty-second cache",
                    within(3, lambda: src_b in peer_rows(PORT)), str(list(peer_rows(PORT))))
    NEW = "what a partner may ask here · the line bee changed"
    st, d = req(PORT_B, "PUT", f"/v1/nodes/{area_b}", {"use_when": NEW})
    check("bee rewrites the line it advertises", 200 <= st < 300, f"{st}")
    check("  and ay reads the new line within three seconds", arrived and within(3, lambda: peer_rows(PORT).get(src_b, {}).get("use_when") == NEW),
          str(peer_rows(PORT).get(src_b, {}).get("use_when"))[:80])
    st, d = req(PORT_B, "PUT", f"/v1/nodes/{area_b}", {"export": "no"})
    check("bee withdraws it", 200 <= st < 300, f"{st}")
    # Only meaningful if it was there to withdraw: a row that never arrived is "gone" for free.
    check("  and it is gone from ay within three seconds", arrived and within(3, lambda: src_b not in peer_rows(PORT)), str(list(peer_rows(PORT))))

    # the control: with bee not knowing ay, there is no poke, and the sixty-second cache is all ay has
    stop(b)
    open(os.path.join(repo_b, "peers.yaml"), "w", encoding="utf-8").write("peers: []\n"); git(repo_b, "commit", "-qam", "bee forgets ay")
    b = start(repo_b, PORT_B, TOKEN_B, {})
    req(PORT_B, "PUT", f"/v1/nodes/{area_b}", {"export": "yes"})
    check("control: with no back-link there is no poke, and the change does NOT reach ay in three seconds",
          not within(3, lambda: src_b in peer_rows(PORT)), "it arrived — then the cache, not the poke, is what carried it, and the check above proves nothing")
    stop(b)
    link(repo_b, "ay", PORT, "PEERTOK_A"); git(repo_b, "commit", "-qam", "bee knows ay again")
    b = start(repo_b, PORT_B, TOKEN_B, {})

    # ── a session follows peers.yaml ──────────────────────────────────────────
    tok = session(PORT, TOKEN_B)
    check("bee's key mints a session on ay", bool(tok))
    st, d = req(PORT, "GET", "/v1/export/regions", token=tok)
    check("  and the session reads ay's export surface", st == 200, f"{st} {json.dumps(d)[:80]}")
    open(os.path.join(repo_a, "peers.yaml"), "w", encoding="utf-8").write("peers: []\n"); git(repo_a, "commit", "-qam", "ay forgets bee")
    st, d = req(PORT, "GET", "/v1/export/regions", token=tok)
    check("ay forgets bee in peers.yaml, by hand and committed: the session is refused on the very next read", st == 401, f"{st} {json.dumps(d)[:100]}")
    st, d = req(PORT, "POST", "/v1/peers/token", token=TOKEN_B)
    check("  and bee's key no longer mints one", st in (401, 403, 501), f"{st} {json.dumps(d)[:100]}")
    link(repo_a, "bee", PORT_B, "PEERTOK_B"); git(repo_a, "commit", "-qam", "ay knows bee again")
    check("  declared again, a new session mints", bool(session(PORT, TOKEN_B)))

    # ── the MCP's area list follows hop 0 ─────────────────────────────────────
    m = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"), "--api", f"http://127.0.0.1:{PORT}/v1", "--actor", "follow-check"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    n = [0]
    def rpc(method, params=None):
        n[0] += 1; m.stdin.write(json.dumps({"jsonrpc": "2.0", "id": n[0], "method": method, "params": params or {}}) + "\n"); m.stdin.flush()
        return json.loads(m.stdout.readline())
    rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "follow-check", "version": "0"}})
    m.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"); m.stdin.flush()
    desc = lambda: rpc("tools/list")["result"]["tools"][0]["description"]
    check("the first tool's description carries hop 0", "/v1/regions/" in desc())
    check("  and not an area that does not exist yet", "/v1/regions/follow-area" not in desc())
    st, d = req(PORT, "POST", "/v1/regions", {"source": "follow-area", "core_description": "Made while the client was connected",
                                             "representative": {"id": "follow-area", "name": "Follow Area", "one_liner": "x", "use_when": "when the check adds an area"}})
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
