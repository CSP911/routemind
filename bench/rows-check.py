#!/usr/bin/env python3
"""Are any two area advertisements near-duplicates in embedding space?

If they are, the router is coin-flipping between them and routing accuracy has a floor that no
better model lifts. Checkable before anything is run, because it depends only on the five sentences
— which are frozen for this experiment.

Three texts per area, because which one the router actually sees depends on how it is built:
  use_when   the sentence written to be routed on
  title+desc what a listing shows
  all        both, which is what hop 0 emits
"""
import json, math, pathlib, re, sys, yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from retrieve import Dense

ROOT = pathlib.Path(__file__).resolve().parent
rj = json.loads((ROOT / "corpus" / "regions.json").read_text(encoding="utf-8"))
rows = {r["source"].replace("_", "-"): r for r in rj["regions"]}

VIEWS = {
    "use_when":   lambda r: r.get("use_when", ""),
    "title+desc": lambda r: f"{r.get('title','')}. {r.get('description','')}",
    "all":        lambda r: f"{r.get('title','')}. {r.get('description','')}. {r.get('use_when','')}",
}
d = Dense()
for view, f in VIEWS.items():
    names = sorted(rows)
    vs = dict(zip(names, d.embed([f(rows[n]) for n in names])))
    pairs = []
    for i, a in enumerate(names):
        for b in names[i+1:]:
            pairs.append((sum(x*y for x, y in zip(vs[a], vs[b])), a, b))
    pairs.sort(reverse=True)
    print(f"\n  {view}")
    for s, a, b in pairs:
        flag = "  <-- too close" if s >= 0.80 else ("  <-- worth a look" if s >= 0.70 else "")
        print(f"      {s:.3f}  {a:<12} {b}{flag}")
    print(f"      mean {sum(p[0] for p in pairs)/len(pairs):.3f}   max {pairs[0][0]:.3f}")
