#!/usr/bin/env python3
"""Aggregate eval/runs/pres-<variant>-r<n>.json into one table: variant × arm → found / operative,
averaged over runs, plus per-question read order for the routing arm."""
import glob, json, pathlib, re, sys, collections
HERE = pathlib.Path(__file__).resolve().parents[2] / "runs"
NAMES = {"a": "a silent", "d": "d dates-in-row", "b": "b doc-header", "c": "c row-statement", "e": "e both"}
agg = collections.defaultdict(lambda: collections.defaultdict(list))   # (variant, arm) -> q -> [(found, beats)]
reads = collections.defaultdict(list)
for f in sorted(glob.glob(str(HERE / "pres-*-r*.json"))):
    m = re.search(r"pres-([a-z])-r(\d+)", f); v, r = m.group(1), m.group(2)
    d = json.load(open(f))
    for row in d["results"]:
        agg[(v, row["arm"])][row["q"]].append((row["found"], row["beats_distractors"]))
        if row["arm"] == "routing": reads[(v, row["q"])].append((r, row.get("read"), row.get("exhausted")))
arms = ["rag", "rag+rerank", "routing"]
print(f"{'variant':<18}" + "".join(f"{a:>22}" for a in arms) + "   (found / operative, mean over runs × 5 questions)")
for v in "adbce":
    line = f"{NAMES[v]:<18}"
    for a in arms:
        qs = agg.get((v, a))
        if not qs: line += f"{'—':>22}"; continue
        fs = [x[0] for q in qs.values() for x in q]; bs = [x[1] for q in qs.values() for x in q]
        n = len(set(len(q) for q in qs.values()))
        line += f"{sum(fs)/len(fs):>10.3f} / {sum(bs)/len(bs):<9.3f}"
    print(line)
print()
qs = sorted({q for (_, q) in reads})
for q in qs:
    print(q[:90])
    for v in "adbce":
        for r, got, ex in reads.get((v, q), []):
            print(f"   {v} r{r}  {'EXHAUSTED ' if ex else ''}read {got}")
