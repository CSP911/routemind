#!/usr/bin/env python3
"""What `rm -rf regions/<area>` leaves behind, and that tidy mends exactly that.

    ./check/tidy-check.py

`data/repo` is meant to be edited by hand. Deleting an area that way leaves `regions.json` listing an
area that is not there, and the repository refuses every write until it is regenerated. (It also used
to leave dangling edges and a CORE.md row; neither file is read since 2026-10-07.)

Half of what is asserted here is that tidy leaves a healthy repository alone. A tool that changes
somebody's repository has to be more careful than one that adds, and "it fixed the problem" says
nothing about what else it did on the way.
"""
import os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                           # noqa: E402
from service.validate import validate                                     # noqa: E402

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
# An older repository still has the two files retired on 2026-10-07. They must be reported as inert
# and left exactly as they are.
open(os.path.join(hurt, "CORE.md"), "w", encoding="utf-8").write("# Core\n\n| Area | What |\n|---|---|\n| `PAYROLL` | pay |\n")
open(os.path.join(hurt, "edges.yaml"), "w", encoding="utf-8").write("- from: a\n  rel: OWNED_BY\n  to: b\n")
as_repo(hurt)
shutil.rmtree(os.path.join(hurt, "regions", area))
# Committed without regenerating, which is what a hand edit does. A hand edit that has not been
# committed is refused by the transaction before anything else — its own correct behaviour, and not
# what this file is about.
subprocess.run(["git", "-C", hurt, "add", "-A"], check=True, capture_output=True)
subprocess.run(["git", "-C", hurt, "-c", "user.name=t", "-c", "user.email=t@l",
                "commit", "-qm", "delete an area by hand"], check=True, capture_output=True)

errs = validate(Store(hurt)).get("errors") or []
check("deleting an area by hand leaves the repository invalid", bool(errs), "it validated")
check("  because regions.json still lists it", any("regions.json" in str(e) for e in errs),
      " | ".join(str(e)[:60] for e in errs[:3]))

# Reporting must not change anything: somebody runs this to find out, not to commit to it.
snap = hashes(hurt)
r = subprocess.run([sys.executable, os.path.join(ROOT, "ontology", "tidy.py"), hurt],
                   capture_output=True, text=True)
out = r.stdout + r.stderr
check("tidy says regions.json is out of step without --fix", "regions.json" in out, out[:160])
check("  and that the old CORE.md and edges.yaml are inert, without touching them",
      "CORE.md is no longer read" in out and "edges.yaml is no longer read" in out, out[:300])
check("  and changes nothing while listing", hashes(hurt) == snap, "it wrote something on a read")
check("  and exits non-zero, so a script notices", r.returncode == 1, str(r.returncode))

r = subprocess.run([sys.executable, os.path.join(ROOT, "ontology", "tidy.py"), hurt, "--fix"],
                   capture_output=True, text=True)
check("--fix goes through the writer and commits it",
      "committed as" in (r.stdout + r.stderr), (r.stdout + r.stderr)[-140:])
check("--fix makes the repository valid again", r.returncode == 0 and not (validate(Store(hurt)).get("errors") or []),
      " | ".join(str(e)[:60] for e in (validate(Store(hurt)).get("errors") or [])[:2]))
after = hashes(hurt)
changed = sorted(k for k in set(after) | set(snap) if after.get(k) != snap.get(k))
check("  and the only file it changed is regions.json", changed == ["regions.json"], str(changed))

shutil.rmtree(T, ignore_errors=True)
print("\n".join(results))
sys.exit(1 if any(x.startswith("FAIL") for x in results) else 0)
