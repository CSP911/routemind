#!/usr/bin/env python3
"""The ceiling on coarse-to-fine: retrieval inside the *correct* area, handed over for free.

    BENCH_EXTRA_CORPUS=bench/corpus-hard ./bench/scoped-ceiling.py --out eval/runs/<date>-scoped-ceiling.json

Asked for on r/Rag (u/nitish-kmr, 2026-10-01), as the cheap way to settle whether "route to the
area, then rag+rerank inside it" is worth building:

    take the 320 indirect questions, filter the index to the correct area for each one, and
    recompute recall@20. No walker, no reranker, no judge, just embeddings over a filtered index.
    Handing it the correct area is generous on purpose, because it upper-bounds what routing to
    the area could buy.

So this hands every question its gold area(s) — `A_true` — and runs the same fused retrieval the
census ran, once over the whole corpus and once restricted to those areas. The gap between the
two columns is the most the area hop could ever recover for retrieval. The reasoning it tests is
the commenter's: `recall@20 ≈ p × min(1, 20/N)`, and narrowing the area moves only the second
term. If recall inside the right area stays near zero, the failure is `p` — the query does not
land in the right document family at all — and no amount of area routing reaches it.

Same corpus as the census, checked by fingerprint rather than assumed: the run refuses to proceed
if the documents it would search are not the ones the census searched.
"""
import argparse, hashlib, json, os, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import yaml
import run as runner
from retrieve import Hybrid

CENSUS_FINGERPRINT = "a84ac6cf463a1a6d"      # eval/runs/2026-09-20b-retrieval-hard.json


def fingerprint(texts):
    h = hashlib.sha256()
    for i in sorted(texts):
        h.update(i.encode()); h.update(texts[i].encode())
    return h.hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", nargs="+", default=["eval/gold/hard.yaml", "eval/gold/hard-temporal.yaml"])
    ap.add_argument("--k", nargs="+", type=int, default=[10, 20])
    ap.add_argument("--out")
    a = ap.parse_args()

    texts, area, one_liner, children, has_body = runner.corpus()
    fp = fingerprint(texts)
    print(f"  corpus {len(texts)} documents · fingerprint {fp}", file=sys.stderr)
    if fp != CENSUS_FINGERPRINT:
        sys.exit(f"  refusing: fingerprint {fp} is not the census's {CENSUS_FINGERPRINT} — "
                 f"set BENCH_EXTRA_CORPUS=bench/corpus-hard so the same documents are searched")

    qs = []
    for g in a.gold:
        qs += yaml.safe_load((ROOT.parent / g).read_text(encoding="utf-8"))["questions"]
    print(f"  {len(qs)} questions from {len(a.gold)} gold file(s)", file=sys.stderr)

    h = Hybrid(texts).warm()
    by_area = {}
    for i, ar in area.items():
        if i in texts: by_area.setdefault(ar, []).append(i)
    kmax = max(a.k)

    results = []
    for n, q in enumerate(qs, 1):
        d_true = set(q["D_true"])
        scope = [i for ar in q["A_true"] for i in by_area.get(ar, [])]
        full = h.search(q["q"], n=kmax)
        inside = h.search(q["q"], scope=scope, n=kmax)
        r = {"id": q["id"], "lever": q["lever"], "family": q.get("family"), "needs": q["needs"],
             "areas": q["A_true"], "scope_size": len(scope)}
        for k in a.k:
            r[f"full@{k}"] = bool(d_true & set(full[:k]))
            r[f"scoped@{k}"] = bool(d_true & set(inside[:k]))
        r["full_rank"] = next((p for p, i in enumerate(full, 1) if i in d_true), None)
        r["scoped_rank"] = next((p for p, i in enumerate(inside, 1) if i in d_true), None)
        results.append(r)
        if n % 50 == 0: print(f"    {n}/{len(qs)}", file=sys.stderr)

    levers = []
    for r in results:
        if r["lever"] not in levers: levers.append(r["lever"])
    print()
    print(f"  {'lever':<10} {'n':>4}  " + "  ".join(f"{'full@'+str(k):>8} {'scoped@'+str(k):>9}" for k in a.k))
    table = {}
    for lv in levers + ["all"]:
        rs = [r for r in results if lv == "all" or r["lever"] == lv]
        row = {"n": len(rs)}
        for k in a.k:
            row[f"full@{k}"] = sum(r[f"full@{k}"] for r in rs) / len(rs)
            row[f"scoped@{k}"] = sum(r[f"scoped@{k}"] for r in rs) / len(rs)
        table[lv] = row
        print(f"  {lv:<10} {len(rs):>4}  " + "  ".join(f"{row[f'full@{k}']:>8.3f} {row[f'scoped@{k}']:>9.3f}" for k in a.k))
    print()
    print("  scoped@20 − full@20 is the most the area hop could buy retrieval, with the area given for free.")

    if a.out:
        p = ROOT.parent / a.out
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"fingerprint": fp, "documents": len(texts), "gold": a.gold, "k": a.k,
                                 "embed_model": h.dense.model, "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                 "asked_by": "u/nitish-kmr on r/Rag, 2026-10-01 (comment pbjo5b6)",
                                 "table": table, "results": results}, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  -> {a.out}")


if __name__ == "__main__":
    main()
