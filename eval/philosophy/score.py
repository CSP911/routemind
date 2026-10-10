#!/usr/bin/env python3
"""Score a philosophy run from what the agent did and said.

    ./eval/philosophy/score.py eval/runs/<date>-philosophy

Per walk: whether the answer matches `expect` and avoids `refuse`, whether the first call was hop 0,
whether every step carried a `why`, how many documents were read, and — for the absent questions —
whether any document was read before saying it is not there. The regexes are a first pass; the README
of the run says where reading the answer disagreed with them.
"""
import json, pathlib, re, sys
import yaml

HERE = pathlib.Path(__file__).resolve().parent
spec = {q["id"]: q for q in yaml.safe_load((HERE / "questions.yaml").read_text())["questions"]}
run = pathlib.Path(sys.argv[1])
rows = []
for f in sorted(run.glob("*-*.json")):
    if f.name == "meta.json": continue
    d = json.loads(f.read_text()); q = spec[d["id"]]; ans = d.get("answer") or ""
    calls = d.get("calls") or []
    hop0 = bool(calls) and calls[0]["tool"] == "knowledge_table" and not calls[0]["input"].get("path")
    whys = all(c["input"].get("why") for c in calls[1:])
    reads = sum(1 for c in calls if c["tool"] == "knowledge_read")
    ok = bool(re.search(q["expect"], ans)) and not (q.get("refuse") and re.search(q["refuse"], ans))
    rows.append((d["model"], d["id"], q["kind"], ok, hop0, whys, len(calls), reads, d.get("cost_usd") or 0))
print(f"{'model':8} {'q':4} {'kind':10} {'pass':5} {'hop0':5} {'why':5} {'calls':>5} {'reads':>5} {'$':>7}")
for r in rows:
    print(f"{r[0]:8} {r[1]:4} {r[2]:10} {str(r[3]):5} {str(r[4]):5} {str(r[5]):5} {r[6]:>5} {r[7]:>5} {r[8]:>7.4f}")
for m in sorted({r[0] for r in rows}):
    mine = [r for r in rows if r[0] == m]
    print(f"{m}: {sum(r[3] for r in mine)}/{len(mine)} pass, hop 0 first {sum(r[4] for r in mine)}/{len(mine)}, "
          f"${sum(r[8] for r in mine):.3f}")
