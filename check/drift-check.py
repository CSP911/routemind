#!/usr/bin/env python3
"""A hand-edited repository, served: what a reader gets when `regions.json` was committed stale.

    ./check/drift-check.py [port]

The validator already caught a stale `regions.json` (ontology/check.py). What it did not do, until
2026-10-05, was change anything a reader saw: the server logged `valid=False` at startup and then
served the committed table to everyone — an `export: yes` somebody had written into an area by hand
and committed never crossed to a peer, and `/healthz` said ok. This starts a real server on a copy
of the shipped repository, in the two states a person actually leaves it in, and reads back what
the server serves and what it did to the disk.

  committed stale   the hand edit is committed. The server must regenerate the table through the
                    ordinary write transaction at startup — one commit, saying why — and then serve
                    and export the area as the file says.
  dirty stale       the hand edit is not committed. The server must not commit anything on the
                    person's behalf, must still serve what the file says, and must say on /healthz
                    that the repository does not validate and how to fix it.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18150
TOKEN = "drift-check-enrolment-key"
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def get(path, token=None):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", headers={"X-Peer-Token": token} if token else {})
    try:
        with urllib.request.urlopen(req, timeout=20) as r: return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout.strip()


def start(repo):
    env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_PEER_TOKEN": TOKEN,
           "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
    log = open(os.path.join(repo, "..", "svc.log"), "a")
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); return p
        except Exception: time.sleep(0.25)
    p.kill(); sys.exit("  the ontology never answered — log:\n" + open(os.path.join(repo, "..", "svc.log")).read()[-1500:])


def stop(p):
    p.terminate()
    try: p.wait(5)
    except Exception: p.kill()


def session():
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/peers/token", data=b"", method="POST", headers={"X-Peer-Token": TOKEN})
    with urllib.request.urlopen(req, timeout=20) as r: return json.loads(r.read())["token"]


T = tempfile.mkdtemp(prefix="drift-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
git(repo, "init", "-q"); git(repo, "config", "user.email", "drift@routemind"); git(repo, "config", "user.name", "drift-check")
# In sync to begin with, whatever the copied install's own table says.
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                            # noqa: E402
from service import derive                                                 # noqa: E402
open(os.path.join(repo, "regions.json"), "w", encoding="utf-8").write(derive.regions_doc(Store(repo)))
git(repo, "add", "-A"); git(repo, "commit", "-qm", "the shipped repository, in sync")
area = sorted(d for d in os.listdir(os.path.join(repo, "regions")) if os.path.isdir(os.path.join(repo, "regions", d)))[0]
md = os.path.join(repo, "regions", area, f"{area}.md")
src = area.replace("-", "_")

try:
    # ── a column the files no longer produce ──────────────────────────────────
    # `description` came from CORE.md, retired 2026-10-07. Every committed table still carried it, and
    # the drift test looked only at the fields the files produce, so it never saw it: startup said
    # valid and healed nothing, and the stale column stayed until somebody happened to write.
    rj = os.path.join(repo, "regions.json")
    doc = json.load(open(rj, encoding="utf-8"))
    for r in doc["regions"]: r["description"] = "a CORE.md row"
    open(rj, "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    git(repo, "commit", "-qam", "a table written before the column was retired")
    before = git(repo, "rev-parse", "HEAD")
    p = start(repo)
    check("a table with a retired column is regenerated at startup, once",
          git(repo, "rev-list", "--count", f"{before}..HEAD") == "1", git(repo, "log", "--oneline", "-3"))
    check("  and the column is gone", all("description" not in r for r in json.load(open(rj, encoding="utf-8"))["regions"]))
    stop(p)

    # ── committed stale ───────────────────────────────────────────────────────
    text = open(md, encoding="utf-8").read()
    assert "\nrole: representative\n" in text, md
    text = text.replace("\nexport: no\n", "\n", 1).replace("\nrole: representative\n", "\nrole: representative\nexport: yes\n", 1)
    open(md, "w", encoding="utf-8").write(text)
    git(repo, "commit", "-qam", "export, written by hand")
    before = git(repo, "rev-parse", "HEAD")
    committed_flag = next(r for r in json.load(open(os.path.join(repo, "regions.json")))["regions"] if r["source"] == src)["export"]
    check("the committed table still says the area is not exported", committed_flag is False, str(committed_flag))

    p = start(repo)
    after = git(repo, "rev-parse", "HEAD")
    check("startup regenerated the table and committed it, once", after != before and git(repo, "rev-list", "--count", f"{before}..HEAD") == "1",
          git(repo, "log", "--oneline", "-3"))
    check("  with a message that says why", "committed stale" in git(repo, "log", "-1", "--format=%s"), git(repo, "log", "-1", "--format=%s"))
    check("  and a clean tree afterwards", git(repo, "status", "--porcelain") == "", git(repo, "status", "--porcelain"))
    st, h = get("/healthz")
    check("/healthz says valid", h.get("valid") is True and h.get("errors") == [], json.dumps({k: h.get(k) for k in ("valid", "errors")}))
    # The hop-0 listing does not carry `export` — whether an area crosses is the owner's view, on the
    # area itself — so the flag is read where it is shown, and the crossing is read where it happens.
    st, one = get(f"/v1/regions/{area}")
    check("the area shows the flag the person wrote", st == 200 and one.get("export") is True, json.dumps({k: one.get(k) for k in ("dir", "export")}))
    st, ex = get("/v1/export/regions", session())
    check("and the area crosses on the export surface", st == 200 and src in [r["source"] for r in ex.get("regions", [])],
          f"{st} {[r.get('source') for r in ex.get('regions', [])]}")
    stop(p)

    # ── dirty stale ───────────────────────────────────────────────────────────
    text = open(md, encoding="utf-8").read()
    open(md, "w", encoding="utf-8").write(text.replace("use_when:", "use_when: EDITED BY HAND ·", 1))
    before = git(repo, "rev-parse", "HEAD")
    p = start(repo)
    check("with uncommitted changes nothing is committed on the person's behalf", git(repo, "rev-parse", "HEAD") == before,
          git(repo, "log", "--oneline", "-2"))
    check("  and the hand edit is still there, uncommitted", "EDITED BY HAND" in open(md, encoding="utf-8").read()
          and git(repo, "status", "--porcelain") != "")
    st, h = get("/healthz")
    check("/healthz says the repository does not validate", h.get("valid") is False, json.dumps({k: h.get(k) for k in ("valid", "errors")})[:200])
    check("  naming the area, the field and the fix", any(f"regions.json {src}" in e and "use_when" in e and "tidy.py" in e for e in h.get("errors", [])),
          json.dumps(h.get("errors"))[:300])
    check("  and says the tree is not writable", h.get("writable") is False, str(h.get("writable")))
    st, d = get("/v1/regions")
    row = next((r for r in d.get("regions", []) if r.get("source") == src), {})
    check("readers are served what the file says, not the stale table", "EDITED BY HAND" in str(row.get("use_when")), str(row.get("use_when"))[:100])
    st, one = get(f"/v1/regions/{area}")
    check("  on both read paths", "EDITED BY HAND" in str(one.get("use_when")), str(one.get("use_when"))[:100])
    log = open(os.path.join(T, "svc.log"), encoding="utf-8", errors="replace").read()
    check("  and the log says so, and how to fix it", "could not be regenerated" in log and "tidy.py" in log)
    stop(p)
finally:
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
