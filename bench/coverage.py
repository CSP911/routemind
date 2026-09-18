#!/usr/bin/env python3
"""Coverage — how specifically the advertisement above a document reaches it.

Two readings, because routing descends a tree rather than stopping at hop 0:

  --hop0    against the area's frozen `use_when`. What the first decision is made on.
  --parent  against the immediate parent's advertisement — its `one_liner` below hop 0,
            since that is the text an area listing prints for each row. The default.

The second is the one the study needs. A document three levels down is never chosen from hop 0; it
is chosen from the row its parent's listing prints for it. Measuring only against hop 0 asks a
question no router ever asks past the first step.

Original note, kept because it is why the measure has the shape it does:

The continuous axis Q2 is drawn against. For a document, the **maximum** similarity over the
clauses of its area's frozen `use_when`, not the similarity to the whole sentence.

The distinction is the whole point and it was found by getting it wrong. Cosine against the whole
description measures topical proximity: `expense` says "how much a business trip pays", and a
document about travel insurance shares the vocabulary of trips and scores close (0.390) while that
clause does not describe it at all. A document about budget variance shares nothing, scores far
(0.344), and is equally uncovered. Taking the max over clauses asks the sharper question — is there
*one specific clause* for this document — rather than is it near the average of five.

    ./bench/coverage.py                 the table, per stratum
    ./bench/coverage.py --per-document  id, area, stratum, coverage — for plotting and for the sample
"""
import argparse, json, pathlib, re, statistics, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from retrieve import Dense
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def load():
    man = json.loads((ROOT / "manifest.json").read_text())
    spec = yaml.safe_load((ROOT / "spec.yaml").read_text(encoding="utf-8"))
    clauses = {a: [c.strip() for c in spec[a]["frozen_use_when"].split("·")] for a in spec}
    texts, ad, parent = {}, {}, {}
    for p in (ROOT / "corpus" / "regions").rglob("*.md"):
        m = FM.match(p.read_text(encoding="utf-8")); fm = yaml.safe_load(m.group(1)) or {}
        i = fm.get("id") or p.stem
        parent[i] = fm.get("parent")
        # What a listing prints for this node: `use_when` where there is one — only the five area
        # representatives have it — and the one-liner everywhere else, which is what
        # mcp/knowledge_mcp.py puts in the `why` column of an area's table.
        ad[i] = fm.get("use_when") or fm.get("one_liner") or ""
        # Section pages are scaffolding this study put there, not documents the corpus is about.
        if i in man and not man[i].get("section"):
            texts[i] = f"{fm.get('name','')}. {fm.get('one_liner','')}\n\n{m.group(2).strip()}"
    return man, clauses, texts, ad, parent


def measure():
    man, clauses, texts, ad, parent = load()
    d = Dense()
    flat = [(a, c) for a, cs in clauses.items() for c in cs]
    cv = dict(zip(flat, d.embed([c for _, c in flat])))
    ids = list(texts)
    dv = dict(zip(ids, d.embed([texts[i] for i in ids])))
    # A parent's advertisement is one sentence, not a list of clauses, so there is nothing to take a
    # maximum over. Splitting on `·` anyway costs nothing and handles the five that are clause lists.
    pads = sorted({ad[parent[i]] for i in ids if parent.get(i) and ad.get(parent[i])})
    pv = dict(zip(pads, d.embed(pads))) if pads else {}
    cos = lambda u, v: sum(x * y for x, y in zip(u, v))
    out = {}
    for i in ids:
        a = man[i]["area"]
        par = parent.get(i)
        out[i] = {"area": a, "stratum": man[i]["stratum"], "cluster": man[i]["cluster"],
                  "parent": par or "",
                  "hop0": max(cos(dv[i], cv[(a, c)]) for c in clauses[a]),
                  "parent_cov": cos(dv[i], pv[ad[par]]) if par and ad.get(par) in pv else None}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-document", action="store_true")
    ap.add_argument("--hop0", action="store_true", help="measure against hop 0 instead of the parent")
    a = ap.parse_args()
    key = "hop0" if a.hop0 else "parent_cov"
    out = {i: r for i, r in measure().items() if r[key] is not None}
    if a.per_document:
        print("id,area,stratum,parent,coverage_parent,coverage_hop0")
        for i, r in sorted(out.items(), key=lambda kv: -kv[1][key]):
            pc = "" if r["parent_cov"] is None else f"{r['parent_cov']:.4f}"
            print(f"{i},{r['area']},{r['stratum']},{r['parent']},{pc},{r['hop0']:.4f}")
        return
    print(f"  {len(out)} documents · measured against "
          f"{'the area row at hop 0' if a.hop0 else 'the advertisement of the immediate parent'}\n")
    print("  stratum    n      this measure     hop 0, for comparison")
    by = {}
    for r in out.values(): by.setdefault(r["stratum"], []).append(r)
    for s in ("S1", "S2", "S3", "S4"):
        v = by.get(s) or []
        if not v: continue
        c = [x[key] for x in v]; h = [x["hop0"] for x in v]
        print(f"  {s:<8} {len(v):>4}   {statistics.mean(c):.3f} (sd {statistics.pstdev(c):.3f})   {statistics.mean(h):.3f}")
    if {"S1", "S2"} <= set(by):
        g = statistics.mean([x[key] for x in by["S1"]]) - statistics.mean([x[key] for x in by["S2"]])
        print(f"\n  S1 − S2 on this measure: {g:+.3f}")
    print("  S2/S3/S4 are expected to sit together: all three are uncovered, and they differ in why.")


if __name__ == "__main__":
    main()
