#!/usr/bin/env python3
"""What an edit made by hand left behind, and — when asked — removing it.

    ./ontology/tidy.py data/repo           say what is left over, change nothing
    ./ontology/tidy.py data/repo --fix     remove it, and regenerate regions.json

`data/repo` is meant to be edited by hand — docs/DATA-REPO.md is a whole document about that, and a
pull request against an ontology is the point. But `rm -rf regions/payroll` leaves two things, and
only one of them was loud:

  * **edges whose ends are gone.** The validator names them, so the repository refuses every write
    until somebody deals with it. Loud, and no way to finish.
  * **a CORE.md row for an area that is not there.** CORE.md is carried *whole* into every prompt and
    its table is where each area's description at hop 0 comes from, so the row goes on advertising
    something that does not exist. This was silent until 2026-09-30.

Nothing is removed without `--fix`, and `--fix` removes only these two things. An edge between two
documents that both still exist is somebody's statement and is never touched; nor is a CORE row whose
area is there. Silent tidying of a repository somebody is editing is how you lose a line they meant.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from service.store import Store                                           # noqa: E402
from service import derive                                               # noqa: E402
from service.write import Writer                                         # noqa: E402


def leftovers(repo: pathlib.Path) -> tuple[list[dict], list[str]]:
    """(edges with an end that is gone, CORE labels with no area). Reads only."""
    store = Store(repo)
    have = {n["id"] for n in store.nodes()}
    dangling = [e for e in store.edges()
                if e.get("from") not in have or e.get("to") not in have]
    on_disk = {derive.region_label(d.name)
               for d in (repo / "regions").iterdir() if d.is_dir()}
    try:
        core = store.core()
    except Exception:
        core = ""
    stale = [m.group(1) for m in re.finditer(r"^\| `([A-Z_]+)` \| .+ \|$", core, re.M)
             if m.group(1) not in on_disk]
    return dangling, stale


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("repo")
    ap.add_argument("--fix", action="store_true",
                    help="remove what is listed, then regenerate, validate and commit")
    ap.add_argument("--actor", default="tidy", help="the name on the commit this makes")
    a = ap.parse_args()
    repo = pathlib.Path(a.repo)
    if not (repo / "regions.json").is_file():
        print(f"  {a.repo} is not a RouteMind repository — no regions.json in it", file=sys.stderr)
        return 2

    dangling, stale = leftovers(repo)
    if not dangling and not stale:
        print("  nothing left over.", file=sys.stderr)
        return 0

    for e in dangling:
        print(f"  edge  {e.get('from')} -{e.get('rel')}-> {e.get('to')}   "
              f"({'from' if e.get('from') else 'to'}-node is gone)", file=sys.stderr)
    for lab in stale:
        print(f"  CORE  `{lab}` is advertised and is not an area here — that table is carried whole "
              f"into every prompt", file=sys.stderr)

    if not a.fix:
        print(f"\n  {len(dangling)} edge(s) and {len(stale)} CORE row(s). "
              f"Nothing was changed; --fix removes exactly these.", file=sys.stderr)
        return 1

    # The same transaction every other write here uses — refuse a dirty tree, mutate, regenerate,
    # validate, roll back on any failure, commit. Removing things from somebody's repository through
    # a path of its own is exactly how the graft ended up with no rollback and no commit.
    writer = Writer(repo)

    def mutate():
        store = Store(repo)
        have = {n["id"] for n in store.nodes()}
        keep = [e for e in store.edges() if e.get("from") in have and e.get("to") in have]
        writer._save_edges(keep)
        core_path = repo / "CORE.md"
        if stale and core_path.is_file():
            text = core_path.read_text(encoding="utf-8")
            for lab in stale:
                text = re.sub(r"^\| `" + re.escape(lab) + r"` \| .+ \|$\n?", "", text, flags=re.M)
            core_path.write_text(text, encoding="utf-8")

    try:
        res = writer.transact(
            f"tidy: {len(dangling)} dangling edge(s), {len(stale)} stale CORE row(s)", a.actor, mutate)
    except Exception as e:
        detail = getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
        rows = getattr(e, "details", None) or []
        print(f"  {detail}" + ("".join(f"\n    · {r}" for r in rows[:8]) if rows else ""), file=sys.stderr)
        print("  Nothing was removed — the repository is as it was.", file=sys.stderr)
        return 1
    print(f"\n  removed {len(dangling)} edge(s) and {len(stale)} CORE row(s), validated, and "
          f"committed as {str(res.get('revision') or '')[:8]}.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
