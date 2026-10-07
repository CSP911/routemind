#!/usr/bin/env python3
"""Invariants 5 and 7: a routing change is a commit, and nothing is reported done that did not happen.

    ./check/transact-check.py [port]

Two halves. The static one reads `ontology/service/write.py` as a syntax tree and asserts that every
public `Writer` method that touches the tree does so inside `transact` — or delegates to one that
does — so a method added later without the transaction fails here before it fails on somebody's
repository. The dynamic one starts a real ontology on a copy of the shipped repository and drives
**every write path there is**: each API write, the proposal queue's accept, and `tidy --fix`. For each: one call that should succeed and one that should fail, and after each the
same three readings — how many commits the repository gained, whether its tree is clean, and what
the response said.

The invariant, as three facts per write:

  success   exactly one commit; the tree is clean; the response's `revision` is that commit
  failure   no commit; the tree is clean (rolled back, or never touched); the response is not 2xx
  always    the response says what the repository says — a 2xx is a commit, a non-2xx is none

The failures are chosen to land in different places on purpose: some are refused before the
transaction opens (a missing field), some inside it after the files were already changed (a parent
that does not exist, which only the validator sees). The second kind is the one that proves the
rollback, and the check counts how many it got.
"""
import ast, json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18210
TOKEN = "transact-check-enrolment-key"
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


# ── static: every writer goes through the transaction ─────────────────────────
src = open(os.path.join(ROOT, "ontology", "service", "write.py"), encoding="utf-8").read()
tree = ast.parse(src)
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Writer")
TOUCHES = ("write_text", "store_write", "write_node_index", "unlink", "rmtree", "mkdir", "rename", "replace")
methods = {fn.name: fn for fn in cls.body if isinstance(fn, ast.FunctionDef)}
def calls(fn): return {ast.unparse(c.func) for c in ast.walk(fn) if isinstance(c, ast.Call)}
def through_transact(name, seen=()):
    fn = methods[name]; cs = calls(fn)
    if any(c.endswith("transact") for c in cs): return True
    # delegation: a public method that only calls another public method which transacts
    for c in cs:
        if c.startswith("self.") and c[5:] in methods and c[5:] not in seen and not c[5:].startswith("_"):
            if through_transact(c[5:], seen + (name,)): return True
    return False
LEGACY = set()     # was the flat fragments directory, retired 2026-10-07
offenders = []
for name, fn in methods.items():
    if name.startswith("_") or name in ("transact",) or name in LEGACY: continue
    touches = sorted(c for c in calls(fn) if any(c.endswith(t) for t in TOUCHES))
    if touches and not through_transact(name): offenders.append(f"{name} ({', '.join(touches[:3])})")
check(f"static: every Writer method that touches the tree goes through transact ({len(methods)} methods read)", not offenders, "; ".join(offenders))
for f in ("ontology/tidy.py",):
    s = open(os.path.join(ROOT, f), encoding="utf-8").read()
    check(f"static: {f} writes through transact", "transact(" in s)

# ── dynamic ───────────────────────────────────────────────────────────────────
T = tempfile.mkdtemp(prefix="transact-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
def git(*a, cwd=repo): return subprocess.run(["git", "-C", cwd, *a], capture_output=True, text=True, check=True).stdout.strip()
for cmd in (["init", "-q"], ["config", "user.email", "tx@routemind"], ["config", "user.name", "transact-check"], ["add", "-A"], ["commit", "-qm", "as shipped"]):
    git(*cmd)
os.makedirs(os.path.join(T, "harness"), exist_ok=True)
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_PEER_TOKEN": TOKEN, "ONTOLOGY_HARNESS": os.path.join(T, "harness"),
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env, stdout=open(os.path.join(T, "svc.log"), "w"), stderr=subprocess.STDOUT)
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else:
    svc.kill(); sys.exit("  the ontology never answered — log:\n" + open(os.path.join(T, "svc.log")).read()[-1500:])


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=data, method=method,
                                 headers={"Content-Type": "application/json", "X-Knowledge-Actor": "transact-check"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}


def head(): return git("rev-parse", "HEAD")
def clean(): return git("status", "--porcelain") == ""
def commits_since(h): return int(git("rev-list", "--count", f"{h}..HEAD"))

rollbacks = 0


def write(name, method, path, body, *, succeed=True):
    """One write, and the three readings after it."""
    global rollbacks
    h0 = head(); st, d = call(method, path, body); n = commits_since(h0)
    if succeed:
        ok = 200 <= st < 300
        check(f"{name}: succeeds", ok, f"{st} {json.dumps(d)[:120]}")
        check(f"  one commit, and the tree is clean", n == 1 and clean(), f"commits {n}, clean {clean()}")
        # The proposal queue wraps the write's result under `result`; the fact is the same.
        rev = d.get("revision") or (d.get("result") or {}).get("revision")
        check(f"  the response names that commit", rev == head(), f"{str(rev)[:10]} vs {head()[:10]}")
    else:
        bad = not (200 <= st < 300)
        check(f"{name}: is refused", bad, f"{st} {json.dumps(d)[:120]}")
        check(f"  no commit, and the tree is clean", n == 0 and clean(), f"commits {n}, clean {clean()}")
        check(f"  and the response says so", bool(d.get("error")) and "revision" not in d, json.dumps(d)[:120])
        if d.get("reason") == "validation_failed" or "validation failed" in str(d.get("error", "")): rollbacks += 1
    return st, d


try:
    # areas
    write("create area", "POST", "/v1/regions", {"source": "tx-area",
          "representative": {"id": "tx-area", "name": "Transact Area", "one_liner": "A place for the check", "use_when": "when the check needs an area"}})
    write("create area (no sentence)", "POST", "/v1/regions", {"source": "tx-area-2",
          "representative": {"name": "X", "one_liner": "x"}}, succeed=False)
    # Refused by the validator only, inside the transaction, so it is rolled back: a `use_when` that is
    # the one-liner again is a description, not a condition.
    write("create area (its condition is its description)", "POST", "/v1/regions", {"source": "tx-area-3",
          "representative": {"id": "tx-area-3", "name": "Y", "one_liner": "same words", "use_when": "same words"}}, succeed=False)
    # nodes
    write("create node", "POST", "/v1/nodes", {"name": "Transact node", "one_liner": "A node for the check", "region": "tx-area", "parent": "tx-area", "content": "# Transact node\n\nWritten 6 October 2026.\n"})
    write("create node (parent does not exist — only the validator sees it)", "POST", "/v1/nodes",
          {"name": "Orphan", "one_liner": "x", "region": "tx-area", "parent": "no-such-parent"}, succeed=False)
    write("update node", "PUT", "/v1/nodes/transact-node", {"one_liner": "A node for the check, revised"})
    write("update node (a field that is not editable)", "PUT", "/v1/nodes/transact-node", {"region": "expense"}, succeed=False)
    # files on a node
    write("put file", "PUT", "/v1/nodes/transact-node/files/note.md", {"content": "# A note\n\nWritten 6 October 2026.\n", "description": "A note under the node"})
    write("put file (bad name)", "PUT", "/v1/nodes/transact-node/files/INDEX.md", {"content": "x", "description": "x"}, succeed=False)
    write("promote file", "POST", "/v1/nodes/transact-node/files/note.md/promote", {"name": "A note, promoted", "one_liner": "The note as a node of its own"})
    write("promote file (not listed)", "POST", "/v1/nodes/transact-node/files/nope.md/promote", {"name": "x", "one_liner": "x"}, succeed=False)
    write("put file (again, to delete it)", "PUT", "/v1/nodes/transact-node/files/note2.md", {"content": "# Two\n\nWritten 6 October 2026.\n", "description": "A second note"})
    write("delete file", "DELETE", "/v1/nodes/transact-node/files/note2.md", None)
    write("delete file (not listed)", "DELETE", "/v1/nodes/transact-node/files/note2.md", None, succeed=False)
    # the proposal queue's accept is a write too
    st, p = call("POST", "/v1/curator/proposals", {"scope": "bb", "region": "tx-area", "after": "when the check needs an area · and when it needs two", "why": "check"})
    pid = p.get("id", "")
    if check("a routing proposal is queued (not a commit yet)", st == 201 and bool(pid) and clean(), json.dumps(p)[:120]):
        write("accept proposal", "POST", f"/v1/curator/proposals/{pid}/accept", {"why": "ok"})
    st, p = call("POST", "/v1/curator/proposals", {"scope": "entity", "entity": "no-such-node", "after": "x", "why": "check"})
    pid2 = p.get("id", "")
    if pid2: write("accept proposal (its entity does not exist)", "POST", f"/v1/curator/proposals/{pid2}/accept", {"why": "ok"}, succeed=False)
    # delete node / area
    write("delete node (promoted child)", "DELETE", "/v1/nodes/a-note-promoted", None)
    write("delete node (gone)", "DELETE", "/v1/nodes/a-note-promoted", None, succeed=False)
    write("delete node", "DELETE", "/v1/nodes/transact-node", None)
    write("delete area", "DELETE", "/v1/regions/tx-area", None)
    write("delete area (gone)", "DELETE", "/v1/regions/tx-area", None, succeed=False)

    # ── the writer outside the service: tidy ───────────────────────────────────
    svc.terminate(); svc.wait(5)          # they take the repository lock themselves
    # an area's sentence changed by hand and committed without regenerating, for tidy to mend
    rp = os.path.join(repo, "regions", "expense", "expense.md")
    _t = open(rp, encoding="utf-8").read()
    open(rp, "w", encoding="utf-8").write(_t.replace("use_when: ", "use_when: edited by hand · ", 1))
    git("commit", "-qam", "a sentence edited by hand")
    h0 = head(); r = subprocess.run([sys.executable, os.path.join(ROOT, "ontology", "tidy.py"), repo, "--fix"], env=env, capture_output=True, text=True)
    check("tidy --fix: one commit, clean tree", r.returncode == 0 and commits_since(h0) == 1 and clean(), (r.stdout + r.stderr)[-200:])
    h0 = head(); r = subprocess.run([sys.executable, os.path.join(ROOT, "ontology", "tidy.py"), repo, "--fix"], env=env, capture_output=True, text=True)
    check("tidy --fix with nothing to do: no commit", commits_since(h0) == 0 and clean(), (r.stdout + r.stderr)[-200:])

    # ── a dirty tree refuses every write, and says so ─────────────────────────
    svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env, stdout=open(os.path.join(T, "svc3.log"), "w"), stderr=subprocess.STDOUT)
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)
    else:
        sys.exit("  the ontology did not come back for the dirty-tree step — log:\n" + open(os.path.join(T, "svc3.log")).read()[-1500:])
    open(os.path.join(repo, "vocab.yaml"), "a", encoding="utf-8").write("\n# edited by hand\n")
    h0 = head(); st, d = call("POST", "/v1/nodes", {"name": "On a dirty tree", "one_liner": "x", "region": "expense", "parent": "expense"})
    check("a hand-edited, uncommitted tree refuses a write", st == 409 and d.get("reason") == "tree_dirty" and commits_since(h0) == 0, f"{st} {json.dumps(d)[:120]}")
    check("  and leaves the hand edit alone", "edited by hand" in open(os.path.join(repo, "vocab.yaml"), encoding="utf-8").read())

    check(f"failures that reached the validator and were rolled back: {rollbacks}", rollbacks >= 2, str(rollbacks))
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
