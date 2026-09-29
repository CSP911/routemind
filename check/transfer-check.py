#!/usr/bin/env python3
"""What an export actually contains, and what it refuses.

    ./check/transfer-check.py [ontology-url]

Everything here was measured by hand once and is kept measured, because the two questions this file
answers are the two a person asks before handing the thing to somebody else: *is all of it in there*,
and *is anything in there that should not be*.

The second question is the one with teeth. An area crosses a link only because somebody wrote
`use_when_export` on it, and this backbone has that line on one area of six. A change that made the
export read the ordinary API — or "helpfully" fall back to it when the export surface 404s — would
widen that silently, and the file would look exactly the same from outside.
"""
import json, os, subprocess, sys, urllib.error, urllib.request

API = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("ROUTEMIND_API", "http://ontology:8100")
TOKEN = os.environ.get("ROUTEMIND_TOKEN", "")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
results = []


def check(name, cond, detail=""):
    results.append(("ok  " if cond else "FAIL") + " " + name)
    if not cond and detail: results.append("     " + detail)
    return cond


def run_in_web(code, env=None):
    """The sealing code lives in the web image, which is where `cryptography` is.

    Run there rather than here: this check has to work on a host python that has neither the library
    nor pyyaml, which is the same reason docs/CHECKS.md splits the suite by where each part can run.
    """
    e = ["-e", f"T={TOKEN}"] + sum((["-e", f"{k}={v}"] for k, v in (env or {}).items()), [])
    p = subprocess.run(["docker", "compose", "exec", "-T", *e, "web", "python3", "-c", code],
                       capture_output=True, text=True, cwd=REPO)
    if p.returncode:
        # A 401 is by far the likeliest failure and it is not what it looks like: the container ran,
        # the code ran, and the token was wrong. Saying "could not run in the web container" over a
        # traceback sends somebody to look at docker.
        if "401" in p.stderr or "peer token" in p.stderr:
            print("FAIL the export surface refused the token — set ROUTEMIND_TOKEN, or "
                  "EXCHANGE_TOKEN_HOME in .env, to one this backbone accepts.", file=sys.stderr)
        else:
            print("FAIL could not run in the web container:\n" + p.stderr[-600:], file=sys.stderr)
        sys.exit(1)
    return p.stdout


COLLECT = """
import sys, os, json
sys.path.insert(0, '/app/transfer')
import bundle
print(json.dumps(bundle.collect(os.environ['API'], os.environ['T']), ensure_ascii=False))
"""

data = json.loads(run_in_web(COLLECT, {"API": API}))

# ---- what is in it -------------------------------------------------------------------------------

check("the export names its format and where it came from",
      data.get("format") == "routemind-export/1" and data.get("source", {}).get("revision"))

ids = {n["id"] for n in data["nodes"] if n.get("id")}
check(f"it carries {len(data['regions'])} area(s) and {len(ids)} node(s)", bool(ids))

# Every node the exported areas hold, not merely every node some list mentioned. The walk follows
# `entries`; this counts the files on disk and asks for the same number. Since the directory→file
# migration a node's "files" are its child nodes, so a gap here is a document that would silently not
# have crossed.
shared = [r.get("source") for r in data["regions"] if r.get("source")]
on_disk = set()
for src in shared:
    d = os.path.join(REPO, "data", "repo", "regions", src)
    if os.path.isdir(d):
        on_disk |= {f[:-3] for f in os.listdir(d) if f.endswith(".md")}
if on_disk:
    check(f"every node the shared area(s) hold is in it ({len(ids & on_disk)}/{len(on_disk)})",
          on_disk <= ids, f"missing {sorted(on_disk - ids)}")
else:
    results.append("--   no shared area on disk to count against; completeness unchecked")

# The links across the tree. Both ends inside the shared set, or it does not cross: an edge naming a
# node in an area nobody shared would say that node exists, and every 404 on that surface is written
# so "we do not have it" and "we did not share it" cannot be told apart. On the shipped corpus four
# edges cross and four more are held back for exactly that reason, so neither side of this is vacuous.
edges = data.get("edges") or []
out_of_set = [e for e in edges if e.get("from") not in ids or e.get("to") not in ids]
check(f"the links between exported documents are in it ({len(edges)})", bool(edges))
check("  and no link names a document outside the export", not out_of_set,
      f"leaked {[f'{e.get(chr(34)+chr(34)) if False else e.get("from")}->{e.get("to")}' for e in out_of_set[:3]]}")

bodies = sum(1 for n in data["nodes"] if (n.get("body") or "").strip())
tables = sum(1 for n in data["nodes"] if n.get("entries"))
check(f"the documents' text is in it, not just their names ({bodies} with a body, {tables} with rows)",
      bodies > 0 and bodies + tables >= len(ids))

# ---- what is not ---------------------------------------------------------------------------------

# The line in the file is the one written for an outside reader. A backbone's own `use_when` is an
# advertisement to its own hop 0 and has no reason to be true anywhere else.
def frontmatter(src, key):
    p = os.path.join(REPO, "data", "repo", "regions", src, src + ".md")
    if not os.path.isfile(p): return None
    for line in open(p, encoding="utf-8"):
        if line.startswith(key + ":"): return line[len(key) + 1:].strip()
    return None


for r in data["regions"]:
    src = r.get("source")
    inward = frontmatter(src, "use_when")
    if inward:
        # One sentence since 2026-09-29: what crosses is the area's own line. This used to check that
        # the *outward* line crossed and the local one did not; it now checks they are the same
        # string, which is the same property — a peer reads the line the area is actually chosen by,
        # never a second copy that can drift from it.
        check(f"the line that crosses is the area's own ({src})",
              (r.get("use_when") or "").strip() == inward.strip(),
              f"crossed {r.get('use_when')!r}, the area says {inward!r}")
        break
else:
    results.append("--   no shared area with a line to compare; unchecked")

# The one that matters. An area with no `use_when_export` is not in the file, whatever else changes.
regions_dir = os.path.join(REPO, "data", "repo", "regions")
all_areas = {d for d in os.listdir(regions_dir) if os.path.isdir(os.path.join(regions_dir, d))} \
    if os.path.isdir(regions_dir) else set()
unshared = {a for a in all_areas if (frontmatter(a, "export") or "").strip().lower() not in ("yes", "true")}
check(f"areas nobody marked to cross are absent ({len(unshared)} of {len(all_areas)} held back)",
      bool(unshared) and not (unshared & set(shared)),
      f"leaked {sorted(unshared & set(shared))}")

# Whatever a node in an unshared area is called, it is not in the file either.
leaked = set()
for a in unshared:
    d = os.path.join(regions_dir, a)
    leaked |= ({f[:-3] for f in os.listdir(d) if f.endswith(".md")} & ids)
check("and so are their documents", not leaked, f"leaked {sorted(leaked)}")

# ---- the file -------------------------------------------------------------------------------------

SEAL = r"""
import sys, os, json, base64
sys.path.insert(0, '/app/transfer')
import bundle
payload = json.loads(os.environ['PAYLOAD'])
blob = bundle.seal(payload, 'correct horse battery staple')
out = {'bytes': len(blob), 'magic': blob[:11].decode('ascii', 'replace')}
out['round_trip'] = bundle.unseal(blob, 'correct horse battery staple') == payload

def refused(b, pw='correct horse battery staple'):
    try:
        bundle.unseal(b, pw); return None
    except bundle.BundleError as e: return str(e)

out['wrong_pass'] = refused(blob, 'the wrong passphrase')
t = bytearray(blob); t[-1] ^= 1
out['body_edited'] = refused(bytes(t))
h = bytearray(blob); i = h.index(b'"n": 131072')
h[i:i+11] = b'"n": 1048576'
out['huge_kdf'] = refused(bytes(h))
out['not_an_export'] = refused(b'hello world')
out['truncated'] = refused(blob[:40])
out['bad_header'] = refused(b'RMEXPORT/1\n{nope}\nxxxx')
print(json.dumps(out, ensure_ascii=False))
"""
SEAL_ONLY = """
import sys, os, json, base64
sys.path.insert(0, '/app/transfer')
import bundle
sys.stdout.write(base64.b64encode(
    bundle.seal(json.loads(os.environ['PAYLOAD']), 'correct horse battery staple')).decode())
"""

r = json.loads(run_in_web(SEAL, {"API": API, "PAYLOAD": json.dumps(data, ensure_ascii=False)}))

check("the file says what it is in its first eleven bytes", r["magic"] == "RMEXPORT/1\n")
check(f"it seals and opens again ({r['bytes']:,} bytes)", r["round_trip"])

# Each of these is a file somebody could be handed. None of them may open, and none may leave as a
# stack trace — on the web endpoint that is a 500 with a traceback instead of a sentence.
for name, key in [("a wrong passphrase", "wrong_pass"), ("an edited body", "body_edited"),
                  ("an edited header", "huge_kdf"), ("something that is not an export", "not_an_export"),
                  ("a truncated file", "truncated"), ("an unreadable header", "bad_header")]:
    check(f"{name} is refused, in a sentence", bool(r[key]), "it opened, or it crashed")

# A wrong passphrase and a tampered file are one failure here, and saying which would be guessing.
check("  and a wrong passphrase reads the same as a tampered one",
      r["wrong_pass"] == r["body_edited"])
# The header's KDF cost is spent before the tag can judge it, so it is read first.
check("  while a header demanding 1GB of key derivation is refused without spending it",
      "over the" in (r["huge_kdf"] or ""))

# ---- grafting into a repository that already has data ------------------------------------------

# The whole point of the prefix. This grafts an export into a copy of a *different* backbone whose
# ids collide with it — 19 of 19 on the corpus this was written against — and asks that backbone's
# own validator whether the result is coherent. Its verdict is the only one that counts: a repository
# it rejects is one the service would refuse to serve.
import hashlib, shutil, tempfile


def _walk_md(root):
    return sorted(os.path.join(r, f) for r, _, fs in os.walk(os.path.join(root, "regions"))
                  for f in fs if f.endswith(".md"))

src_repo = os.path.join(REPO, "data-b", "repo")
if not os.path.isdir(src_repo):
    results.append("--   no second repository to graft into; the graft path is unchecked")
else:
    tmp = tempfile.mkdtemp()
    target = os.path.join(tmp, "repo")
    shutil.copytree(src_repo, target)
    try:
        before_docs = len(_walk_md(target))
        before_state = {q: hashlib.sha256(open(q, "rb").read()).hexdigest() for q in _walk_md(target)}
        blob = run_in_web(SEAL_ONLY, {"API": API, "PAYLOAD": json.dumps(data, ensure_ascii=False)})
        bundle_path = os.path.join(tmp, "b.rmx")
        with open(bundle_path, "wb") as f:
            f.write(__import__("base64").b64decode(blob))

        env = dict(os.environ, ROUTEMIND_EXPORT_PASSPHRASE="correct horse battery staple",
                   PYTHONPATH=os.path.join(REPO, "pylib"))
        p = subprocess.run([sys.executable, os.path.join(REPO, "transfer", "import.py"), bundle_path,
                            "--graft", target, "--prefix", "partner"],
                           capture_output=True, text=True, env=env, cwd=REPO)
        out = p.stdout + p.stderr
        check("a graft into a repository with colliding ids succeeds", p.returncode == 0, out[-300:])
        check("  and that repository validates afterwards", "The repository validates." in out,
              "its own validator rejected the result")

        after_docs = len(_walk_md(target))
        check(f"  every node arrived ({after_docs - before_docs} added)",
              after_docs - before_docs == len(ids))

        # The originals must be exactly as they were. A graft that edited them would be a merge, and
        # which of two same-named subjects owns a name is a decision, not something to do quietly.
        #
        # Hashed before and after rather than read from `git status`: the fixture is a copy of a live
        # repository and can carry uncommitted work of its own, which git reports and this must not.
        # It said so once — a field migration in the source showed up here as a file the graft had
        # edited, which it had not touched.
        after_state = {q: hashlib.sha256(open(q, "rb").read()).hexdigest()
                       for q in _walk_md(target) if "partner-" not in q}
        touched = sorted(q[len(target) + 1:] for q in after_state
                         if before_state.get(q) != after_state[q])
        check("  and nothing that was already there was edited", not touched, f"edited {touched[:5]}")

        # The links must arrive renamed with the documents, or they point at the receiver's own
        # same-named documents — which is the collision the prefix exists to prevent, reappearing
        # through the back door.
        ed = os.path.join(target, "edges.yaml")
        text = open(ed, encoding="utf-8").read() if os.path.isfile(ed) else ""
        got = text.count("from: partner-")
        check(f"  and the links between them came too ({got})", got == len(edges))
        check("  with both ends renamed", "to: partner-" in text and text.count("to: partner-") == got)

        # The same prefix twice must not quietly overwrite the first graft.
        p2 = subprocess.run([sys.executable, os.path.join(REPO, "transfer", "import.py"), bundle_path,
                             "--graft", target, "--prefix", "partner"],
                            capture_output=True, text=True, env=env, cwd=REPO)
        check("grafting the same bundle under the same prefix is refused",
              p2.returncode != 0 and "still collide" in (p2.stdout + p2.stderr),
              "it would have overwritten the first graft")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

print("\n".join(results))
sys.exit(1 if any(x.startswith("FAIL") for x in results) else 0)
