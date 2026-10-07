#!/usr/bin/env python3
"""An area whose directory has a hyphen, on every path that used to spell it two ways.

    ./check/hyphen-check.py [port]

Reported by a user, 2026-10-07: "derive.py turns the hyphens in `source` into underscores when it
writes regions.json." So an area `back-office` was `back_office` in its `source`, and every reader
that took `source` for the directory name was wrong for exactly the hyphenated areas. The one that
broke: the export surface compared a node's area (`back-office`) with the source (`back_office`), so
every node of an exported hyphenated area was a 404 to every reader while the area's table read fine.

`source` is now the directory name, as it is, and readers accept the old spelling because committed
tables and older backbones still carry it. This checks:

  one spelling       a hyphenated area's source is its directory, in regions.json and on every read
  a circuit          another backbone reads the area, its representative, a node and its body
  an old table       a regions.json committed in the old spelling is caught by the validator, served
                     in the new one meanwhile, and regenerated at startup
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18420
TOKEN = "hyphen-check-key"
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def git(repo, *a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout.strip()


def call(method, path, body=None, token=None, raw=False):
    r = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=json.dumps(body).encode() if body is not None else None, method=method,
                               headers={"Content-Type": "application/json", "X-Knowledge-Actor": "hyphen-check", **({"X-Peer-Token": token} if token else {})})
    try:
        with urllib.request.urlopen(r, timeout=30) as x:
            b = x.read(); return x.status, (b.decode() if raw else json.loads(b or b"{}"))
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}


T = tempfile.mkdtemp(prefix="hyphen-check-")
env = {**os.environ, "PORT": str(PORT), "ONTOLOGY_PEER_TOKEN": TOKEN,
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
procs = []


def start(repo):
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env={**env, "ONTOLOGY_DATA": repo},
                         stdout=open(os.path.join(T, "svc.log"), "a"), stderr=subprocess.STDOUT)
    procs.append(p)
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); return p
        except Exception: time.sleep(0.25)
    sys.exit("  the ontology never answered — " + open(os.path.join(T, "svc.log")).read()[-1200:])


def stop(p):
    p.terminate()
    try: p.wait(5)
    except Exception: p.kill()


try:
    repo = os.path.join(T, "repo")
    shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
    git(repo, "init", "-q"); git(repo, "config", "user.email", "h@r"); git(repo, "config", "user.name", "h"); git(repo, "add", "-A"); git(repo, "commit", "-qm", "as shipped")
    p = start(repo)

    # ── one spelling ──────────────────────────────────────────────────────────
    st, _ = call("POST", "/v1/regions", {"source": "back-office", "representative": {"id": "back-office", "name": "Back Office", "one_liner": "Keys and access",
                                    "use_when": "who opens the office · a key is lost", "export": "yes"}})
    call("POST", "/v1/nodes", {"name": "Spare keys", "one_liner": "Where the spare keys are kept", "region": "back-office",
                               "parent": "back-office", "content": "# Spare keys\n\nWritten 7 October 2026.\n"})
    rj = json.load(open(os.path.join(repo, "regions.json")))
    row = next((r for r in rj["regions"] if "back" in r["source"]), {})
    check("a hyphenated area's source is its directory name in regions.json", st == 201 and row.get("source") == "back-office", json.dumps(row)[:120])
    st, top = call("GET", "/v1/regions")
    check("  and on hop 0", any(r["source"] == "back-office" for r in top.get("regions", [])))

    # ── across a link ─────────────────────────────────────────────────────────
    st, s = call("POST", "/v1/peers/token", token=TOKEN); sess = s.get("token", "")
    st, ex = call("GET", "/v1/export/regions", token=sess)
    check("a peer is advertised the area under its directory name", any(r["source"] == "back-office" for r in ex.get("regions", [])),
          str([r["source"] for r in ex.get("regions", [])]))
    for path, what in [("/v1/export/regions/back-office", "the area's table"), ("/v1/export/nodes/back-office", "its representative"),
                       ("/v1/export/nodes/spare-keys", "a node in it"), ("/v1/export/nodes/spare-keys/body", "that node's document")]:
        st, _ = call("GET", path, token=sess, raw=path.endswith("/body"))
        check(f"  a peer reads {what}", st == 200, f"{st} on {path}")
    stop(p)

    # ── an old table ──────────────────────────────────────────────────────────
    rj = json.load(open(os.path.join(repo, "regions.json")))
    for r in rj["regions"]:
        r["source"] = r["source"].replace("-", "_")
    open(os.path.join(repo, "regions.json"), "w", encoding="utf-8").write(json.dumps(rj, indent=1, ensure_ascii=False) + "\n")
    git(repo, "commit", "-qa", "--allow-empty", "-m", "regions.json, as derive wrote it before 2026-10-07")
    sys.path.insert(0, os.path.join(ROOT, "ontology"))
    from service.store import Store
    from service.validate import validate
    v = validate(Store(repo))
    check("a table committed in the old spelling is caught by the validator", not v["ok"] and any("back-office" in e and "source" in e for e in v["errors"]),
          json.dumps(v["errors"][:2])[:200])
    before = git(repo, "rev-parse", "HEAD")
    p = start(repo)
    rj = json.load(open(os.path.join(repo, "regions.json")))
    check("  and regenerated at startup, in one commit", git(repo, "rev-parse", "HEAD") != before and next(r for r in rj["regions"] if "back" in r["source"])["source"] == "back-office")
    st, s = call("POST", "/v1/peers/token", token=TOKEN)
    st, _ = call("GET", "/v1/export/nodes/spare-keys", token=s.get("token", ""))
    check("  after which a peer still reads its nodes", st == 200, str(st))

finally:
    for p in procs:
        try: stop(p)
        except Exception: pass
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
