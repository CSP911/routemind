#!/usr/bin/env python3
"""The export surface answers only what was shared — by every address it has, not only the listed ones.

    ./check/export-check.py [port]

docs/CIRCUIT.md: a kind marked `export: no` never crosses, and neither does a draft or anything under
either. The surface was right for `nodes/<id>` and wrong one segment further down: the old spelling
`nodes/<parent>/files/<child>.md` reached the ordinary reader, which checked the parent and served
the child's file raw, frontmatter and all — a draft, or a kind that does not cross, read by anyone
holding a session (audit SV-2, 2026-11-02). This exports one area of a copy of the shipped corpus
with one kind denied and one entity drafted, and asks for each of them at every address the surface
might answer.
"""
import json, os, re, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18160
TOKEN = "export-check-enrolment-key"
TTL = 120          # not six hours, so a refusal that names six hours is caught saying it
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def call(path, token=None, method="GET"):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", method=method, data=(b"" if method == "POST" else None),
                                 headers={"X-Peer-Token": token} if token else {})
    try:
        with urllib.request.urlopen(req, timeout=20) as r: return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e: return e.code, e.read().decode("utf-8", "replace")


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout.strip()


T = tempfile.mkdtemp(prefix="export-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "examples", "back-office"), repo)
git(repo, "init", "-q"); git(repo, "config", "user.email", "export@routemind"); git(repo, "config", "user.name", "export-check")


def edit(rel, f):
    p = os.path.join(repo, rel)
    with open(p, encoding="utf-8") as fh: t = fh.read()
    with open(p, "w", encoding="utf-8") as fh: fh.write(f(t))


# Expenses crosses; `case` does not; one procedure is a draft.
edit("regions/expense/expense.md", lambda t: t.replace("\nrole: representative\n", "\nrole: representative\nexport: yes\n", 1))
edit("vocab.yaml", lambda t: re.sub(r"(- id: case\n  desc: [^\n]*\n)", r"\1  export: no\n", t, count=1))
edit("regions/expense/card-lost-steps.md", lambda t: t.replace("\nparent: card-loss\n", "\nparent: card-loss\nstatus: draft\n", 1))
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                            # noqa: E402
from service import derive                                                 # noqa: E402
with open(os.path.join(repo, "regions.json"), "w", encoding="utf-8") as fh: fh.write(derive.regions_doc(Store(repo)))
git(repo, "add", "-A"); git(repo, "commit", "-qm", "expenses exported, cases kept in, one draft")

env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_PEER_TOKEN": TOKEN,
       "ONTOLOGY_PEER_SESSION_TTL": str(TTL),
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
log = open(os.path.join(T, "svc.log"), "w")
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env, stdout=log, stderr=subprocess.STDOUT)
try:
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)
    else:
        sys.exit("FAIL the ontology never answered — log:\n" + open(os.path.join(T, "svc.log")).read()[-1500:])

    st, body = call("/v1/peers/token", TOKEN, "POST")
    if not check("a session is minted", st == 200, f"HTTP {st} {body[:120]}"):
        raise SystemExit
    s = json.loads(body)["token"]

    # ---- what is shared is served --------------------------------------------------------------
    check("an exported entity reads", call("/v1/export/nodes/travel-overseas", s)[0] == 200)
    check("  and its document", call("/v1/export/nodes/card-loss/body", s)[0] == 200)
    st, body = call("/v1/export/nodes/travel-overseas", s)
    check("  its table leaves out the kind that does not cross",
          st == 200 and "case-overseas-settlement" not in body, body[:200])

    # ---- what is not shared is refused, at every address ---------------------------------------
    for what, path in [
        ("a denied kind, by its own address", "/v1/export/nodes/case-overseas-settlement"),
        ("a denied kind, as a file of its parent", "/v1/export/nodes/travel-overseas/files/case-overseas-settlement.md"),
        ("under a denied kind, as a file of it", "/v1/export/nodes/case-overseas-settlement/files/case-lost-receipt.md"),
        ("a draft, by its own address", "/v1/export/nodes/card-lost-steps"),
        ("a draft, as a file of its parent", "/v1/export/nodes/card-loss/files/card-lost-steps.md"),
        ("a shared child by the old file spelling — one shape of address, not two",
         "/v1/export/nodes/corp-card/files/card-loss.md"),
        ("a path the surface does not have", "/v1/export/nodes/card-loss/body/extra"),
    ]:
        st, body = call(path, s)
        check(f"{what}: 404", st == 404, f"HTTP {st} {body[:160]!r}")
        check("  and nothing of it in the answer", "---\nid:" not in body and "\n# " not in body, body[:160])

    # ---- the refusal tells the truth about how long a session lasts ----------------------------
    st, body = call("/v1/export/regions", "not-a-session")
    check("a read without a session is refused", st == 401, f"HTTP {st}")
    check("  and the refusal names the configured lifetime, not six hours",
          "six hours" not in body and "2 minutes" in body, body[:240])
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    print("\n".join(results))
    shutil.rmtree(T, ignore_errors=True)

sys.exit(1 if not results or any(r.startswith("FAIL") for r in results) else 0)
