#!/usr/bin/env python3
"""What `rm -rf regions/<area>` leaves behind, and that tidy removes exactly that.

    ./check/tidy-check.py

`data/repo` is meant to be edited by hand. Deleting an area that way leaves two things, and until
2026-09-30 only one of them was loud:

  * edges whose ends are gone — the validator names them, so the repository refuses every write
  * a CORE.md row for an area that is not there — **silent**, and CORE.md is carried whole into every
    prompt, so hop 0 went on advertising something that did not exist

Half of what is asserted here is that tidy leaves a healthy repository alone. A tool that removes
things from somebody's repository has to be more careful than one that adds, and "it fixed the
problem" says nothing about what else it did on the way.
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                           # noqa: E402
from service.validate import validate                                     # noqa: E402
from service import derive                                                # noqa: E402

results = []


def check(name, cond, detail=""):
    results.append(("ok  " if cond else "FAIL") + " " + name)
    if not cond and detail: results.append("     " + detail)
    return cond


def hashes(root):
    out = {}
    for base, _, files in os.walk(root):
        if ".git" in base.split(os.sep): continue
        for f in files:
            p = os.path.join(base, f)
            out[os.path.relpath(p, root)] = open(p, "rb").read()
    return out


T = tempfile.mkdtemp()
src = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(src):
    print("FAIL examples/back-office is missing; nothing to work against", file=sys.stderr)
    sys.exit(1)

# ---- a healthy repository is left exactly alone ------------------------------------------------
def as_repo(path):
    """A git repository, because tidy goes through the writer's transaction now and that refuses a
    tree it cannot commit into — the same refusal every other write here makes."""
    subprocess.run(["git", "-C", path, "init", "-q"], check=True)
    subprocess.run(["git", "-C", path, "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", path, "-c", "user.name=t", "-c", "user.email=t@l",
                    "commit", "-qm", "seed"], check=True, capture_output=True)


well = os.path.join(T, "well")
shutil.copytree(src, well)
as_repo(well)
before = hashes(well)
r = subprocess.run([sys.executable, os.path.join(ROOT, "ontology", "tidy.py"), well, "--fix"],
                   capture_output=True, text=True)
check("a healthy repository reports nothing left over",
      r.returncode == 0 and "nothing left over" in (r.stdout + r.stderr), (r.stdout + r.stderr)[:120])
check("  and --fix on it changes no byte", hashes(well) == before,
      str(sorted(set(hashes(well)) ^ set(before))[:3]))

# ---- an area deleted by hand --------------------------------------------------------------------
hurt = os.path.join(T, "hurt")
shutil.copytree(src, hurt)
area = "payroll"
as_repo(hurt)
shutil.rmtree(os.path.join(hurt, "regions", area))
open(os.path.join(hurt, "regions.json"), "w", encoding="utf-8").write(derive.regions_doc(Store(hurt)))
# Committed, because a hand edit that has not been committed is refused by the transaction before
# anything else — which is its own correct behaviour and not what this file is about.
subprocess.run(["git", "-C", hurt, "add", "-A"], check=True, capture_output=True)
subprocess.run(["git", "-C", hurt, "-c", "user.name=t", "-c", "user.email=t@l",
                "commit", "-qm", "delete an area by hand"], check=True, capture_output=True)

errs = validate(Store(hurt)).get("errors") or []
check("deleting an area by hand leaves the repository invalid", bool(errs), "it validated")
# The one that used to be silent. CORE.md goes into every prompt whole.
check("  and the CORE row it left is one of the errors",
      any("CORE.md advertises" in str(e) for e in errs),
      " | ".join(str(e)[:60] for e in errs[:3]))
check("  as are the edges whose ends are gone",
      any(str(e).startswith("edge ") for e in errs), str(errs[:1]))

# Reporting must not change anything: somebody runs this to find out, not to commit to it.
snap = hashes(hurt)
r = subprocess.run([sys.executable, os.path.join(ROOT, "ontology", "tidy.py"), hurt],
                   capture_output=True, text=True)
out = r.stdout + r.stderr
check("tidy lists both kinds without --fix", "CORE" in out and "edge" in out, out[:160])
check("  and changes nothing while listing", hashes(hurt) == snap, "it wrote something on a read")
check("  and exits non-zero, so a script notices", r.returncode == 1, str(r.returncode))

r = subprocess.run([sys.executable, os.path.join(ROOT, "ontology", "tidy.py"), hurt, "--fix"],
                   capture_output=True, text=True)
check("--fix goes through the writer and commits it",
      "committed as" in (r.stdout + r.stderr), (r.stdout + r.stderr)[-140:])
check("--fix makes the repository valid again", r.returncode == 0 and not (validate(Store(hurt)).get("errors") or []),
      " | ".join(str(e)[:60] for e in (validate(Store(hurt)).get("errors") or [])[:2]))
core = open(os.path.join(hurt, "CORE.md"), encoding="utf-8").read()
check("  with the stale CORE row gone", not re.search(r"^\| `PAYROLL` \|", core, re.M))
check("  and the rows for areas that are still here kept",
      len(re.findall(r"^\| `[A-Z_]+` \| ", core, re.M)) == 4,
      str(re.findall(r"^\| `([A-Z_]+)` \|", core, re.M)))
# The half that matters as much: an edge between two documents that both exist is somebody's
# statement, and tidy must not have taken it as collateral.
kept = Store(hurt).edges()
have = {n["id"] for n in Store(hurt).nodes()}
check("  and every surviving edge still has both ends",
      all(e["from"] in have and e["to"] in have for e in kept), str(len(kept)))
check("  while edges it had nothing to do with are still there", len(kept) > 0, str(len(kept)))

shutil.rmtree(T, ignore_errors=True)
print("\n".join(results))
sys.exit(1 if any(x.startswith("FAIL") for x in results) else 0)
