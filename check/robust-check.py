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
  broken file   one hand edit that does not parse used to take every request down and crash-loop the
                restart; it is now left out, named with its line, and writes wait for the fix
  starting over ontology/reset.sh empties the map or puts the example back in one commit, tagging what
                was there; before it, starting over was 79 deletes or a hand edit that left it read-only
  area switch   a walk that leaves one area for another is told so, so a false hop-0 sentence gets reported
  the agent     in token mode the MCP server sent no secret, so an agent could read but not place, and
                its walks went unrecorded; it sends KNOWLEDGE_TOKEN now
"""
import http.server, json, os, urllib.error, shutil, signal, subprocess, sys, tempfile, threading, time, urllib.request

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
    # A server left over from an interrupted run answers on the port and the checks then read *its*
    # repository — which is how this check once failed four times for the wrong reason.
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1)
        sys.exit(f"  port {port} already answers — a server from an earlier run? lsof -ti tcp:{port} | xargs kill")
    except urllib.error.URLError: pass
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

    # ── one file that does not parse ──────────────────────────────────────────
    # A hand edit with an unclosed quote took every request down (502, no file named) and the restart
    # after it crash-looped. Now: the service starts, serves the rest, names the file, refuses writes
    # until it is fixed, and a revert is all it takes. A broken regions.json is derived: regenerated.
    bk = repo_from(ex, "broken")
    f = os.path.join(bk, "regions", "expense", "travel-expense.md"); good = open(f).read()
    open(f, "w").write(good.replace("\nname: ", '\nname: "Broken: [unclosed\n#', 1)); git(bk, "commit", "-qam", "broken by hand")
    p = start(bk, PORT + 3)
    def get(path, port=PORT + 3):
        try: rr = urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=10); return rr.status, json.loads(rr.read())
        except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b"{}")
    h = health(PORT + 3)
    st, regs = get("/v1/regions"); st2, appr = get("/v1/regions/approval")
    check("one file whose frontmatter does not parse: the service starts and serves every other area",
          st == 200 and len(regs.get("regions", [])) == 5 and st2 == 200, f"{st} {st2}")
    check("  its health names the file and the line, and says how to undo the commit",
          any("regions/expense/travel-expense.md" in e and "line" in e and "revert" in e for e in h.get("errors", [])), json.dumps(h)[:300])
    req = urllib.request.Request(f"http://127.0.0.1:{PORT + 3}/v1/nodes/approval", method="PUT", data=b'{"one_liner": "x"}', headers={"Content-Type": "application/json"})
    try: urllib.request.urlopen(req, timeout=10); wst, wbody = 200, ""
    except urllib.error.HTTPError as e: wst, wbody = e.code, e.read().decode()
    check("  a write is refused while it is broken, and the refusal names the file", wst in (409, 422) and "travel-expense.md" in wbody, f"{wst} {wbody[:200]}")
    git(bk, "revert", "--no-edit", "HEAD")
    h = health(PORT + 3)
    check("  `git revert` of the commit that broke it is the whole recovery", h.get("valid") is True, json.dumps(h)[:300])
    # Two shapes the first fix missed (operator QA, 2026-10-10): a byte that is not UTF-8, and a field
    # that is a list. Both still took every request down.
    for label, mangle in (("a byte that is not UTF-8", lambda b: b.replace(b"\nname: ", b"\nname: \xff\xfe", 1)),
                          ("`parent` written as a list", lambda b: b.replace(b"\nparent: ", b"\nparent: [", 1).replace(b"\nkind:", b"\nkind:", 1))):
        raw = open(f, "rb").read()
        new = mangle(raw)
        if b"parent: [" in new:      # close the list on the same line
            i = new.index(b"parent: [") ; j = new.index(b"\n", i); new = new[:j] + b"]" + new[j:]
        open(f, "wb").write(new); git(bk, "commit", "-qam", f"broken: {label}")
        st, regs = get("/v1/regions"); h = health(PORT + 3)
        check(f"  {label}: the rest is served, and the file is named",
              st == 200 and len(regs.get("regions", [])) == 5 and any("travel-expense.md" in e for e in h.get("errors", [])),
              f"{st} {json.dumps(h.get('errors'))[:200]}")
        git(bk, "revert", "--no-edit", "HEAD")
    p.terminate(); p.wait(5)
    open(os.path.join(bk, "regions.json"), "w").write("{not json"); git(bk, "commit", "-qam", "regions.json broken by hand")
    p = start(bk, PORT + 3); h = health(PORT + 3)
    check("  a regions.json broken by hand is regenerated at boot, like any stale derived table",
          h.get("valid") is True and json.load(open(os.path.join(bk, "regions.json"))).get("regions"), json.dumps(h.get("errors"))[:300])
    p.terminate(); p.wait(5)

    # ── an area deleted or added by hand ──────────────────────────────────────
    ha = repo_from(ex, "handarea")
    shutil.rmtree(os.path.join(ha, "regions", "payroll")); git(ha, "add", "-A"); git(ha, "commit", "-qm", "payroll removed by hand")
    p = start(ha, PORT + 5); h = health(PORT + 5)
    left = [r["source"] for r in json.load(open(os.path.join(ha, "regions.json")))["regions"]]
    check("an area deleted by hand and committed: the next start regenerates regions.json and is valid",
          h.get("valid") is True and "payroll" not in left and len(left) == 4, json.dumps(h.get("errors"))[:300])
    p.terminate(); p.wait(5)

    # ── starting over ─────────────────────────────────────────────────────────
    rs = repo_from(ex, "reset")
    p = start(rs, PORT + 4)
    def settle(want, tries=40):
        for _ in range(tries):
            if regions_n() == want and health(PORT + 4).get("valid"): return
            time.sleep(0.25)
    def regions_n():
        return len(json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT + 4}/v1/regions", timeout=10).read()).get("regions", []))
    def reset(*a): return subprocess.run([os.path.join(ROOT, "ontology", "reset.sh"), "--repo", rs, *a], capture_output=True, text=True)
    open(os.path.join(rs, "regions", "expense", "scratch.md"), "w").write("x")
    out = reset("--empty", "--yes")
    check("reset refuses a tree with uncommitted changes and touches nothing", out.returncode != 0 and regions_n() == 5, out.stderr[-200:])
    os.remove(os.path.join(rs, "regions", "expense", "scratch.md"))
    out = reset("--empty", "--yes"); settle(0); h = health(PORT + 4)
    tag = next((l.split()[-1] for l in out.stdout.splitlines() if "reset --hard" in l), "")
    check("reset --empty: one commit, no areas, valid and writable while the service runs",
          out.returncode == 0 and regions_n() == 0 and h.get("valid") and h.get("writable"), out.stderr[-200:] + json.dumps(h)[:200])
    out = reset("--example", "--yes"); settle(5); h = health(PORT + 4)
    check("  reset --example on top of it replaces, not merges: five areas, valid", out.returncode == 0 and regions_n() == 5 and h.get("valid"), json.dumps(h)[:200])
    git(rs, "reset", "-q", "--hard", tag); settle(5)
    check("  and the tag it printed brings the map before it back", tag.startswith("before-reset-") and regions_n() == 5 and health(PORT + 4).get("valid"), tag)
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

    # ── the walk names an area switch ─────────────────────────────────────────
    # eval/philosophy M3: sent into the wrong area by a false hop-0 sentence, neither model reported it
    # until the server pointed out the switch. No note on the first area, nor on going back to it.
    out = subprocess.run([sys.executable, "-c", "import sys, json; sys.path.insert(0, 'mcp'); import knowledge_mcp as M; w = {}; "
                          "print(json.dumps([M.second_area_note(w, p) for p in ('/v1/regions/payroll', '/v1/nodes/insurance', "
                          "'/v1/regions/attendance', '/v1/regions/payroll')]))"], cwd=ROOT, env=env0, capture_output=True, text=True)
    try: notes = json.loads(out.stdout)
    except Exception: notes = []
    check("a walk that switches areas is told which area it entered first, once per switch",
          len(notes) == 4 and notes[0] == "" and notes[1] == "" and "entered payroll first" in notes[2]
          and "entered attendance first" in notes[3], out.stderr[-200:] or notes)
finally:
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
