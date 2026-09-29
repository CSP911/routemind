#!/usr/bin/env python3
"""The two times on a routing row, and the one thing they must never say.

    ./check/age-check.py

An agent reading a table sees `AGE` as `<route> / <document>`: how long this path has been here, and
when what it points at last moved. The pair exists because one number cannot say both — a route laid
down in 2023 over material rewritten last week is current, and the same route over a document that
has not moved is the one worth asking about.

Most of what is checked here is about **not known**. A row whose history cannot be read must not come
out looking like a fresh one: that is the failure that would make this feature worse than having no
dates at all, because a reader would prefer the row the system knows least about.

It builds its own repository and commits into it, so the ages are facts this check made rather than
whatever the shipped data happens to have — on a repo whose history was created in one go, every row
reads the same and nothing here would be distinguishable from a stub.
"""
import os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ontology"))
sys.path.insert(0, os.path.join(ROOT, "mcp"))
from service import ages                                                  # noqa: E402
import knowledge_mcp as mcp                                               # noqa: E402

results = []


# Printed however this ends. A check that dies instead of reporting looks, to anyone reading the
# output, exactly like a check that never ran — and the bug this file exists to hold down is one that
# raises rather than returning something wrong.
import atexit, traceback                                                  # noqa: E402


@atexit.register
def _report():
    if results: print("\n".join(results))


sys.excepthook = lambda k, v, t: (
    results.append("FAIL the check crashed: " + "".join(traceback.format_exception_only(k, v)).strip()),
    sys.stderr.write("".join(traceback.format_exception(k, v, t))))


def check(name, cond, detail=""):
    results.append(("ok  " if cond else "FAIL") + " " + name)
    if not cond and detail: results.append("     " + detail)
    return cond


T = tempfile.mkdtemp()
repo = os.path.join(T, "repo")
os.makedirs(os.path.join(repo, "regions", "area"))


def write(nid, body, when):
    p = os.path.join(repo, "regions", "area", nid + ".md")
    open(p, "w", encoding="utf-8").write(f"---\nid: {nid}\nname: \"{nid}\"\n---\n{body}\n")
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@l",
                    "commit", "-qm", f"{nid} {when}"], check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when})


subprocess.run(["git", "-C", repo, "init", "-q"], check=True, capture_output=True)
# Three shapes, and the middle one is the whole feature: a path laid down long ago whose document
# moved yesterday. Without it "old" and "stale" are the same word.
write("settled", "written once, never touched", "2023-01-05T00:00:00Z")
write("revised", "the original", "2023-01-05T00:00:00Z")
write("recent", "laid down last month", "2026-09-01T00:00:00Z")
write("revised", "the original\n\nrewritten", "2026-09-28T00:00:00Z")

a = ages.of(repo, "probe-1")
check("every document has both times",
      all((a.get(n) or {}).get("route_since") and (a.get(n) or {}).get("changed")
          for n in ("settled", "revised", "recent")), str(a))
check("  a route laid down in 2023 says 2023",
      (a["settled"]["route_since"] or "").startswith("2023"), str(a["settled"]))
# The one the pair exists for.
check("a rewritten document keeps its old route and gets a new changed",
      (a["revised"]["route_since"] or "").startswith("2023")
      and (a["revised"]["changed"] or "").startswith("2026"), str(a["revised"]))
check("  while the one nobody touched keeps both in 2023",
      (a["settled"]["changed"] or "").startswith("2023"), str(a["settled"]))

# ---- what it must never claim -------------------------------------------------------------------
# A repository with no history at all. Every age is unknown, and unknown has to survive all the way
# to the page as unknown — the failure to prevent is a row with no history rendering as the newest
# thing on the table.
bare = os.path.join(T, "bare")
os.makedirs(os.path.join(bare, "regions", "area"))
open(os.path.join(bare, "regions", "area", "x.md"), "w").write("---\nid: x\n---\n")
check("a repository with no git history answers nothing rather than failing",
      ages.of(bare, "probe-2") == {}, str(ages.of(bare, "probe-2")))
check("  and an unknown age renders as `—`, not as blank or today",
      mcp._age({}) == "—", repr(mcp._age({})))
check("  and a half-known one says which half is missing",
      "?" in mcp._age({"changed": "2026-09-01T00:00:00Z"}), repr(mcp._age({"changed": "2026-09-01T00:00:00Z"})))

# The rendered table: the column, and the sentence that says what it means. A column of `3y / 2d`
# with nothing explaining it is read as one number printed twice.
rows = [mcp._row({**a["settled"], "type": "data", "fetch": "/v1/nodes/settled/body", "name": "settled"}),
        mcp._row({**a["revised"], "type": "data", "fetch": "/v1/nodes/revised/body", "name": "revised"}),
        mcp._row({"type": "data", "fetch": "/v1/nodes/far/body", "name": "far"})]
text = mcp._table(rows, "T", "lead", None)
check("the table prints an AGE column", "AGE" in text, text[:120])
check("  and says what the two halves are",
      "how long this route has been here" in text and "document last changed" in text)
check("  and says what `—` means, when one is on the page",
      "not known here" in text and "not the same as new" in text)
# Compared as whole lines rather than by splitting on whitespace: the age is `3y / 3y`, three tokens
# with spaces in it, so `split()[2]` reads `3y` for both rows and the check passes on rows that are
# identical. It did, for one revision — the assertion was wrong while the feature was right.
_settled = next(l for l in text.splitlines() if "/v1/nodes/settled/" in l)
_revised = next(l for l in text.splitlines() if "/v1/nodes/revised/" in l)
check("  and the settled row reads differently from the revised one",
      "3y / 3y" in _settled and "3y / " in _revised and "3y / 3y" not in _revised,
      f"{_settled.strip()}  ||  {_revised.strip()}")

# A node that has **both** a body and children. Its first row is its own document, and that row is
# the node rather than one of its entries — written against the loop variable at first, which is an
# UnboundLocalError and a 500 on every such node.
#
# Checked here, with a stub, because the repository the suite runs against has none: `data/repo` has
# 0 nodes of this shape and the shipped example has 42, so twenty-five suites passed over a path they
# could not reach. A clean install caught it on its first boot.
class _StubApi:
    def json(self, path):
        return {"id": "both", "name": "Both", "body": "it has a document too",
                "route_since": "2023-01-05T00:00:00Z", "changed": "2026-09-28T00:00:00Z",
                "entries": [{"id": "kid", "name": "Kid", "type": "data",
                             "fetch": "/v1/nodes/kid/body", "one_liner": "a child",
                             "route_since": "2023-01-05T00:00:00Z",
                             "changed": "2023-01-05T00:00:00Z"}]}
    def text(self, path): return ""


both = mcp.node(_StubApi(), "/v1/nodes/both")
check("a node with a body and children renders", "/v1/nodes/both/body" in both, both[:150])
check("  and its own row carries its own age, not an entry's",
      any("/v1/nodes/both/body" in l and "1d" in l or "/v1/nodes/both/body" in l and "today" in l
          for l in both.splitlines()),
      "\n".join(l for l in both.splitlines() if "/v1/nodes/" in l))

# A table of rows that all lack ages must not grow an empty column.
plain = mcp._table([{"kind": "file", "address": "/a", "why": "w"}], "T", "l", None)
check("a table with no ages at all prints no AGE column", "AGE" not in plain, plain[:110])

shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
