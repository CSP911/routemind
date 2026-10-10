#!/usr/bin/env python3
"""Compare the same questions on a small map and a large one.

    ./eval/scale/score.py eval/runs/<date>-scale-5areas eval/runs/<date>-scale-30areas

Per walk: the first area entered (the hop-0 decision), whether it was the right one or the lure next
door, whether the answer is right, and what it cost.
"""
import json, pathlib, re, sys
import yaml

HERE = pathlib.Path(__file__).resolve().parent
spec = {q["id"]: q for q in yaml.safe_load((HERE / "questions.yaml").read_text())["questions"]}


def first_area(calls):
    for c in calls:
        m = re.match(r"^/v1/regions/([^/]+)/?$", str(c["input"].get("path") or ""))
        if m: return m.group(1)
    return None


summary = {}
for run in sys.argv[1:]:
    run = pathlib.Path(run); print(f"\n{run.name}")
    print(f"  {'model':7} {'q':4} {'first area':18} {'right':6} {'lure':5} {'answer':7} {'calls':>5} {'$':>7}")
    for f in sorted(run.glob("*-s*.json")):
        d = json.loads(f.read_text()); q = spec[d["id"]]; calls = d.get("calls") or []
        fa = first_area(calls); right = fa == q["area"]; lure = fa == q.get("lure")
        ok = bool(re.search(q["expect"], d.get("answer") or ""))
        s = summary.setdefault((run.name, d["model"]), [0, 0, 0, 0, 0.0, 0])
        s[0] += 1; s[1] += right; s[2] += lure; s[3] += ok; s[4] += d.get("cost_usd") or 0; s[5] += len(calls)
        print(f"  {d['model']:7} {d['id']:4} {str(fa):18} {str(right):6} {str(lure):5} {str(ok):7} {len(calls):>5} {d.get('cost_usd') or 0:>7.4f}")
print()
for (run, m), (n, right, lure, ok, cost, calls) in sorted(summary.items()):
    print(f"{run:28} {m:7} first area right {right}/{n} · lure {lure}/{n} · answer {ok}/{n} · {calls / n:.1f} calls · ${cost:.3f}")
