#!/usr/bin/env python3
"""What an operator meets when things go wrong, or get big — the 2026-10-10 robustness pass.

    ./check/robust-check.py

  interrupted   a write killed between its files and its commit left a dirty tree and an index lock,
                and every write after it was refused as "someone edited the repository by hand". The
                next boot rolls back a write of its own (a marker says so) and nothing else: a real
                hand edit, with no marker, stays exactly as it is
  SIGTERM       as PID 1 with no handler the signal was ignored, so every restart was a SIGKILL after
                ten seconds; idle, it now exits at once
  a wide table  on a map of a few thousand entities, a 200-row table took 20 seconds — the whole node
                list deep-copied once per row; it must stay well under two
  the agent     in token mode the MCP server sent no secret, so an agent could read but not place, and
                its walks went unrecorded; it sends KNOWLEDGE_TOKEN now
"""
import http.server, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 18280
results = []
def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {str(extra)[:220]}"))

T = tempfile.mkdtemp(prefix="robust-check-")
env0 = {**os.environ, "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
for k in [k for k in env0 if k.startswith("ONTOLOGY_LLM_")]: env0.pop(k)


def git(repo, *a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout.strip()


def repo_from(src, name):
    r = os.path.join(T, name); shutil.copytree(src, r)
    for cmd in (["init", "-q"], ["config", "user.email", "r@r"], ["config", "user.name", "robust"], ["add", "-A"], ["commit", "-qm", "start"]):
        git(r, *cmd)
    return r


def start(repo, port):
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                         env={**env0, "ONTOLOGY_DATA": repo, "PORT": str(port)},
                         stdout=open(os.path.join(T, f"svc-{port}.log"), "w"), stderr=subprocess.STDOUT)
    for _ in range(160):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); return p
        except Exception: time.sleep(0.25)
    p.kill(); sys.exit("  the ontology never answered — " + open(os.path.join(T, f"svc-{port}.log")).read()[-1200:])


def health(port): return json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=5).read())


try:
    ex = os.path.join(ROOT, "examples", "back-office")
    # ── an interrupted write is rolled back at boot ───────────────────────────
    r = repo_from(ex, "interrupted")
    open(os.path.join(r, "regions", "expense", "half-written.md"), "w").write("---\nid: half-written\nname: Half\nkind: rule\none_liner: half\nparent: expense\n---\nx\n")
    git(r, "add", "-A")
    open(os.path.join(r, ".git", "index.lock"), "w").write("")
    open(os.path.join(r, ".git", "routemind-transaction"), "w").write("node expense: file half-written.md")
    p = start(r, PORT)
    h = health(PORT)
    check("a write the last process did not finish is rolled back at boot: clean, writable, no lock left",
          h.get("writable") is True and not os.path.exists(os.path.join(r, "regions", "expense", "half-written.md"))
          and not os.path.exists(os.path.join(r, ".git", "index.lock")) and git(r, "status", "--porcelain") == "", json.dumps(h)[:200])
    # ── SIGTERM, idle: out at once ────────────────────────────────────────────
    t0 = time.time(); p.send_signal(signal.SIGTERM)
    try: p.wait(5); took = time.time() - t0
    except subprocess.TimeoutExpired: p.kill(); took = 99
    check("SIGTERM with no write running exits at once, not after a ten-second kill", took < 2, f"{took:.1f}s")

    # ── a hand edit, no marker, is never touched ──────────────────────────────
    r2 = repo_from(ex, "handedit")
    f = os.path.join(r2, "regions", "expense", "expense.md")
    open(f, "a").write("\nA person's unfinished sentence.\n")
    p = start(r2, PORT + 1)
    h = health(PORT + 1)
    check("  while a hand edit with no marker stays as it is, and writes are refused until it is committed",
          h.get("writable") is False and "unfinished sentence" in open(f).read(), json.dumps(h)[:200])
    p.terminate(); p.wait(5)

    # ── a wide table on a large map ───────────────────────────────────────────
    big = repo_from(ex, "big")
    d = os.path.join(big, "regions", "expense")
    open(os.path.join(d, "wide.md"), "w").write("---\nid: wide\nname: Wide\nkind: topic\none_liner: two hundred rows\nparent: expense\n---\n")
    for i in range(200):
        open(os.path.join(d, f"wide-{i:03d}.md"), "w").write(f"---\nid: wide-{i:03d}\nname: Wide row {i}\nkind: rule\none_liner: row {i} of a wide table\nparent: wide\n---\n# Row {i}\n\nbody\n")
    for a in range(10):
        ad = os.path.join(big, "regions", f"filler-{a}"); os.makedirs(ad)
        open(os.path.join(ad, f"filler-{a}.md"), "w").write(f"---\nid: filler-{a}\nname: Filler {a}\nkind: topic\none_liner: filler area {a}\nrole: representative\nuse_when: when filler {a} is asked about\n---\n# F\n\nx\n")
        for i in range(150):
            open(os.path.join(ad, f"filler-{a}-{i}.md"), "w").write(f"---\nid: filler-{a}-{i}\nname: Filler {a} doc {i}\nkind: rule\none_liner: filler document {i}\nparent: filler-{a}\n---\n# D\n\nbody {i}\n")
    git(big, "add", "-A"); git(big, "commit", "-qm", "big")
    p = start(big, PORT + 2)
    urllib.request.urlopen(f"http://127.0.0.1:{PORT + 2}/v1/nodes/wide", timeout=60).read()       # warm
    t0 = time.time(); body = urllib.request.urlopen(f"http://127.0.0.1:{PORT + 2}/v1/nodes/wide", timeout=60).read(); took = time.time() - t0
    check("a 200-row table on a map of ~1,800 entities answers well under two seconds", took < 2 and len(json.loads(body)["entries"]) == 200, f"{took:.2f}s")
    p.terminate(); p.wait(5)

    # ── the MCP server sends the write secret ─────────────────────────────────
    seen = []
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            seen.append(self.headers.get("Authorization") or "")
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b'{"regions": []}')
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    out = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, 'mcp'); import knowledge_mcp as M; M.Api(sys.argv[1], 'robust').json('/v1/regions')",
                          f"http://127.0.0.1:{srv.server_address[1]}"], cwd=ROOT, env={**env0, "KNOWLEDGE_TOKEN": "s3cret"}, capture_output=True, text=True)
    check("the MCP server sends KNOWLEDGE_TOKEN as a bearer secret", seen and seen[-1] == "Bearer s3cret", f"{seen} {out.stderr[-200:]}")
finally:
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
