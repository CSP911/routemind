#!/usr/bin/env python3
"""Which half of the retriever fails, and how far out the failures land. Costs nothing.

Every vector this needs is already in `embeddings.json`, and BM25 is pure python, so this runs with
no API access at all — which is how it came to be written: both providers' balances ran out mid
search and this was the work that was still possible.

It exists to answer the question the ceiling argument raises. `probe.py` measured

    A=3   fusion recall@10 0.35 · recall@20 0.80 · B1 hit@10 0.80

so the reranker recovers **everything** fusion puts in its top 20 and nothing it does not. B1 is
therefore fusion recall@20 to within measurement noise, and breaking B1 means driving recall@20
below 0.50 — a target that can be measured for free.

So: when a paraphrased question buries its answer, which half buried it? If BM25 collapses and dense
holds, the corpus needs documents that are semantically crowded rather than lexically distant. If
both collapse together, wording is the whole story and only a harder corpus will move it.

    ./bench/decompose.py
"""
import json, pathlib, statistics, sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import probe
from retrieve import BM25, Dense, rrf


def rank_of(ranked, doc):
    return ranked.index(doc) + 1 if doc in ranked else None


def main():
    texts, area, raw = probe.corpus_texts()
    rows = json.loads((ROOT / "probe-results-fusion.json").read_text())
    bm = BM25(texts)
    dn = Dense()
    ids = list(texts)
    # Nothing is embedded here: every document and every probe question is already in the cache.
    # `use_cache` is left on and a miss would raise on the key, which is the behaviour wanted — a
    # silent API call is what this whole script is avoiding.
    vecs = {i: dn.cache[dn.cache_key(texts[i])] for i in ids
            if dn.cache_key(texts[i]) in dn.cache}
    missing = [r for r in rows if dn.cache_key(r["q"]) not in dn.cache]
    if missing:
        print(f"  {len(missing)} questions are not in the embedding cache; skipped", file=sys.stderr)

    per = defaultdict(lambda: defaultdict(list))
    for r in rows:
        k = dn.cache_key(r["q"])
        if k not in dn.cache: continue
        qv = dn.cache[k]
        dense = [i for _, i in sorted(((sum(a*b for a, b in zip(qv, vecs[i])), i)
                                       for i in vecs), reverse=True)[:50]]
        sparse = [i for _, i in bm.search(r["q"])[:50]]
        fused = [i for _, i in rrf([dense, sparse])[:50]]
        per[r["A"]]["dense"].append(rank_of(dense, r["doc"]))
        per[r["A"]]["bm25"].append(rank_of(sparse, r["doc"]))
        per[r["A"]]["fused"].append(rank_of(fused, r["doc"]))

    def recall(v, k): return sum(1 for x in v if x and x <= k) / len(v)

    print("\n  which half finds the answer, by how far the wording has moved\n")
    print("        n     BM25@20   dense@20   fused@20  |  BM25@10  dense@10  fused@10")
    for A in sorted(per):
        p = per[A]; n = len(p["fused"])
        print(f"   A={A} {n:>4}     {recall(p['bm25'],20):5.2f}     {recall(p['dense'],20):5.2f}"
              f"      {recall(p['fused'],20):5.2f}   |   {recall(p['bm25'],10):5.2f}    "
              f"{recall(p['dense'],10):5.2f}     {recall(p['fused'],10):5.2f}")

    print("\n  median rank of the answer (999 = outside the top 50)\n")
    print("        BM25   dense   fused")
    for A in sorted(per):
        p = per[A]
        m = lambda v: statistics.median([x or 999 for x in v])
        print(f"   A={A}  {m(p['bm25']):>5.0f}   {m(p['dense']):>5.0f}   {m(p['fused']):>5.0f}")

    print("\n  fusion is worth having only where the two halves disagree:")
    for A in sorted(per):
        p = per[A]
        both = sum(1 for a, b in zip(p["bm25"], p["dense"]) if (a and a <= 20) and (b and b <= 20))
        one = sum(1 for a, b in zip(p["bm25"], p["dense"])
                  if bool(a and a <= 20) != bool(b and b <= 20))
        none = sum(1 for a, b in zip(p["bm25"], p["dense"])
                   if not (a and a <= 20) and not (b and b <= 20))
        n = len(p["fused"])
        print(f"   A={A}   both halves have it {both/n:.0%} · one does {one/n:.0%} · "
              f"neither {none/n:.0%}   <- neither is the only unrecoverable case")


if __name__ == "__main__":
    main()
