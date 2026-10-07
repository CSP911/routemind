#!/usr/bin/env python3
"""What an edit made by hand left behind, and — when asked — mending it.

    ./ontology/tidy.py data/repo           say what is out of step, change nothing
    ./ontology/tidy.py data/repo --fix     regenerate regions.json, validate and commit

`data/repo` is meant to be edited by hand — docs/DATA-REPO.md is a whole document about that, and a
pull request against an ontology is the point. What a hand edit can leave behind is one thing:
`regions.json`, the derived area list, no longer saying what the files say — an area deleted with
`rm -rf regions/payroll` and still listed, or a `use_when` changed in the file and not in the table.
The validator names it, and every write is refused until it is mended. The service also mends it at
startup on a clean tree; this is the same mend without restarting anything.

Until 2026-10-07 this also removed edges whose ends were gone and CORE.md rows with no area. Neither
file is read any more, so neither can be out of step. An old `edges.yaml` or `CORE.md` is reported
as inert and never touched — delete it yourself if you like.

Nothing changes without `--fix`.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from service.store import Store                                           # noqa: E402
from service import derive                                               # noqa: E402
from service.write import Writer                                         # noqa: E402

RETIRED = ("CORE.md", "edges.yaml")


def stale(repo: pathlib.Path) -> bool:
    """Does regions.json say something other than what the files say? Reads only."""
    p = repo / "regions.json"
    return (p.read_text(encoding="utf-8") if p.exists() else "") != derive.regions_doc(Store(repo))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("repo")
    ap.add_argument("--fix", action="store_true",
                    help="regenerate regions.json, then validate and commit")
    ap.add_argument("--actor", default="tidy", help="the name on the commit this makes")
    a = ap.parse_args()
    repo = pathlib.Path(a.repo)
    if not (repo / "regions.json").is_file():
        print(f"  {a.repo} is not a RouteMind repository — no regions.json in it", file=sys.stderr)
        return 2

    for name in RETIRED:
        if (repo / name).exists():
            print(f"  {name} is no longer read (retired 2026-10-07) — inert; delete it if you like",
                  file=sys.stderr)
    if not stale(repo):
        print("  nothing left over.", file=sys.stderr)
        return 0

    print("  regions.json no longer says what the files say.", file=sys.stderr)
    if not a.fix:
        print("  Nothing was changed; --fix regenerates it.", file=sys.stderr)
        return 1

    # The same transaction every other write here uses — refuse a dirty tree, regenerate, validate,
    # roll back on any failure, commit. There is nothing to mutate: regenerating is part of it.
    try:
        res = Writer(repo).transact("tidy: regions.json regenerated from the files", a.actor, lambda: None)
    except Exception as e:
        detail = getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
        rows = getattr(e, "details", None) or []
        print(f"  {detail}" + ("".join(f"\n    · {r}" for r in rows[:8]) if rows else ""), file=sys.stderr)
        print("  Nothing was changed — the repository is as it was.", file=sys.stderr)
        return 1
    print(f"\n  regenerated, validated, and committed as {str(res.get('revision') or '')[:8]}.",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
