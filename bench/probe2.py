#!/usr/bin/env python3
"""The other levers. Does anything except wording break plain RAG?

`probe.py` swept the lexical bridge and found the only cliff in the scale: fusion recall@10 goes
1.00 / 1.00 / 0.94 / 0.39 across A=0..3, while the three document-side factors — depth, routing
margin, crowding — are flat at 0.80-0.96 from C+D+E 0 to 9 with no trend at all. One factor does
everything and four do nothing, which is why summing them equally produced a difficulty axis that
was flat from 4 to 10.

Before the scale is rewritten around A, the factors that were *measured* as doing nothing are given
a fair chance to do something, because there is a real possibility the measurement was wrong rather
than the factor. E scored crowding by counting embedding neighbours; a question does not fail
because a document has neighbours, it fails because the question cannot distinguish between them,
and no question in the sweep was written to be indistinguishable. Same for B: area spread was never
swept at all.

So two levers, each written deliberately and each at two wordings:

    near    a question only one document in a crowded cluster answers, where the siblings all look
            like they might. The distinguishing detail is a qualifier — a grade, a threshold, a date,
            an employment type — and not the subject.
    two     a question that is incompletely answered by either of two documents in different areas.
            Scored both ways: `all` (both retrieved) and `any` (either).

    x A=0   the document's own vocabulary
    x A=3   a full paraphrase

Two by two, so the interaction is visible: if crowding only bites once the wording is also far, that
is a different scale from one where it bites on its own.

    ./bench/probe2.py gen
    ./bench/probe2.py run [--rerank]
    ./bench/probe2.py report
"""
import argparse, collections, json, pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import probe
from retrieve import Hybrid
from rerank import LLMReranker

QUESTIONS = ROOT / "probe2-questions.json"
RESULTS = ROOT / "probe2-results.json"
N_NEAR, N_TWO = 30, 30
MIN_CLUSTER = 8

NEAR_SYSTEM = (
 "You write evaluation questions that a keyword-and-embedding retriever should find hard.\n\n"
 "You are given a TARGET document and several SIBLING documents from the same cluster. Write a "
 "question that:\n"
 "- is answered by the TARGET and by nothing else,\n"
 "- would look, to a reader who had not checked, as though any of the siblings might answer it,\n"
 "- turns on a specific qualifier in the target — a threshold, a grade, a date, an employment type, "
 "a currency, a headcount — rather than on the subject, because the subject is what the siblings "
 "share.\n"
 "- is one sentence, and is a question a person would actually ask.\n\n"
 "Write it twice. Version 0 uses the target's own vocabulary. Version 3 is a full paraphrase that "
 "uses none of the target's distinctive words — the situation described in plain language, by "
 "somebody who knows their problem and not this system's terms. The fact asked for is identical in "
 "both.\n\n"
 "Reply with JSON only: {\"0\": \"...\", \"3\": \"...\"}")

TWO_SYSTEM = (
 "You write evaluation questions that need two sources.\n\n"
 "You are given documents A and B, which live in different areas of a knowledge base. Write one "
 "question that:\n"
 "- cannot be answered completely from A alone or from B alone — each holds a necessary half,\n"
 "- is a single natural question, not two questions joined by 'and',\n"
 "- is something a person in this situation would genuinely need both halves of.\n\n"
 "Write it twice. Version 0 uses the documents' own vocabulary. Version 3 is a full paraphrase using "
 "none of their distinctive words. The fact asked for is identical in both.\n\n"
 "Reply with JSON only: {\"0\": \"...\", \"3\": \"...\"}")


def clusters(man, texts):
    by = collections.defaultdict(list)
    for i, r in sorted(man.items()):
        if r.get("section") or i not in texts: continue
        by[r.get("cluster")].append(i)
    return {c: v for c, v in by.items() if c and len(v) >= MIN_CLUSTER}


def cmd_gen(a):
    texts, area, raw = probe.corpus_texts()
    man = json.loads((ROOT / "manifest.json").read_text())
    out = json.loads(QUESTIONS.read_text()) if QUESTIONS.exists() else {}

    cl = clusters(man, texts)
    # Deterministic: the largest clusters first, one target each, and the target is the middle
    # document so it is neither the cluster's first nor its last by id.
    near = [(c, v[len(v) // 2], [x for x in v if x != v[len(v) // 2]][:6])
            for c, v in sorted(cl.items(), key=lambda kv: -len(kv[1]))[:N_NEAR]]

    # Cross-area pairs: one representative document per cluster, paired across areas. Walked as a
    # round robin over the distinct area pairs so that one fat area does not supply half the set.
    rep = collections.defaultdict(list)
    for c, v in sorted(cl.items()): rep[area[v[0]]].append(v[0])
    areas = sorted(rep)
    apairs = [(x, y) for n, x in enumerate(areas) for y in areas[n + 1:]]
    two, depth = [], 0
    while len(two) < N_TWO and depth < 40:
        for x, y in apairs:
            if len(two) >= N_TWO: break
            if depth < len(rep[x]) and depth < len(rep[y]):
                two.append((rep[x][depth], rep[y][depth]))
        depth += 1

    todo = ([("near", t, sib) for _, t, sib in near if f"near:{t}" not in out] +
            [("two", p, None) for p in two if f"two:{p[0]}|{p[1]}" not in out])
    print(f"  {len(near)} near · {len(two)} two · {len(todo)} to write", file=sys.stderr)
    for n, (kind, target, sibs) in enumerate(todo, 1):
        if kind == "near":
            key = f"near:{target}"
            body = ("TARGET:\n\n" + raw[target][:4000] + "\n\nSIBLINGS:\n\n" +
                    "\n\n".join(raw[s][:900] for s in sibs))
            sysmsg, gold = NEAR_SYSTEM, [target]
        else:
            x, y = target
            key = f"two:{x}|{y}"
            body = ("A:\n\n" + raw[x][:3500] + "\n\nB:\n\n" + raw[y][:3500])
            sysmsg, gold = TWO_SYSTEM, [x, y]
        txt = probe.ask(body, system=sysmsg)
        m = re.search(r"\{.*\}", txt, re.S)
        if not m: print(f"    {key}: no JSON", file=sys.stderr); continue
        try: qs = json.loads(m.group(0))
        except json.JSONDecodeError: print(f"    {key}: bad JSON", file=sys.stderr); continue
        out[key] = {"kind": kind, "gold": gold, "q": {k: qs[k] for k in ("0", "3") if k in qs}}
        QUESTIONS.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    {n}/{len(todo)}  {key}", file=sys.stderr)


def cmd_run(a):
    texts, area, raw = probe.corpus_texts()
    fac = probe.factors()
    qs = json.loads(QUESTIONS.read_text())
    h = Hybrid(texts).warm()
    rr = LLMReranker() if a.rerank else None
    flat = [(k, v, rung, q) for k, v in sorted(qs.items()) for rung, q in sorted(v["q"].items())]
    h.dense.embed([q for _, _, _, q in flat])
    done = {}
    if RESULTS.exists():
        for r in json.loads(RESULTS.read_text()):
            if not a.rerank or "b1" in r: done[(r["key"], r["rung"])] = r
    rows = []
    for n, (key, v, rung, q) in enumerate(flat, 1):
        if (key, int(rung)) in done: rows.append(done[(key, int(rung))]); continue
        fused = h.search(q, n=50)
        gold = v["gold"]
        r = {"key": key, "kind": v["kind"], "rung": int(rung), "q": q, "gold": gold,
             "A": probe.measured_A(q, " ".join(texts[d] for d in gold)),
             "CDE": max(int(fac[d]["CDE"]) for d in gold),
             "fusion": {d: (fused.index(d) + 1 if d in fused else None) for d in gold}}
        if rr is not None:
            ranked = rr.rank(q, fused[:20], texts) + fused[20:]
            r["b1"] = {d: (ranked.index(d) + 1 if d in ranked else None) for d in gold}
        rows.append(r)
        if n % 10 == 0 or n == len(flat):
            RESULTS.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"    {n}/{len(flat)}", file=sys.stderr)
    RESULTS.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")


def cmd_report(a):
    rows = json.loads(RESULTS.read_text())
    field = "b1" if any("b1" in r for r in rows) else "fusion"
    print(f"\n  {len(rows)} probes · scored on {'B1 (fused 20 -> reranked)' if field=='b1' else 'fusion only'}\n")

    def hit_all(r, k): return all(v and v <= k for v in r[field].values())
    def hit_any(r, k): return any(v and v <= k for v in r[field].values())

    for kind in ("near", "two"):
        sub = [r for r in rows if r["kind"] == kind and field in r]
        if not sub: continue
        print(f"  {kind}   n={len(sub)}")
        print("    rung   measured A     hit@10 (all)   hit@10 (any)   hit@20 (all)")
        for rung in (0, 3):
            s = [r for r in sub if r["rung"] == rung]
            if not s: continue
            am = sum(r["A"] for r in s) / len(s)
            print(f"      {rung}      {am:4.1f}          {sum(hit_all(r,10) for r in s)/len(s):5.2f}"
                  f"          {sum(hit_any(r,10) for r in s)/len(s):5.2f}"
                  f"          {sum(hit_all(r,20) for r in s)/len(s):5.2f}   n={len(s)}")
        print()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gen")
    r = sub.add_parser("run"); r.add_argument("--rerank", action="store_true")
    sub.add_parser("report")
    a = ap.parse_args()
    {"gen": cmd_gen, "run": cmd_run, "report": cmd_report}[a.cmd](a)
