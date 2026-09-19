#!/usr/bin/env python3
"""Where the embedding model cannot tell two documents apart. Costs nothing.

`decompose.py` split the retriever in half and found that a full paraphrase destroys BM25
(recall@20 0.13, median rank outside the top 50) and barely touches the dense side (recall@20 0.95,
median rank 3). The lexical axis the difficulty scale was built on is a measure of BM25's problem,
not of retrieval's.

To break retrieval, the *dense* half has to fail, and it fails where two documents mean nearly the
same thing. This finds those places using vectors already in the cache — no API call, which is how
it came to be written.

It also states the hypothesis the next round tests, so that it is on record before the round runs:

    A=3 alone          kills BM25, dense survives, hybrid survives -> measured: B1 0.80
    near alone         dense struggles, but BM25 matches the qualifier exactly ("grade 3", "90 days")
                       and rescues it
    A=3 x near         paraphrase removes the exact terms BM25 needs, and semantic near-duplication
                       removes the separation dense needs. **Both halves fail at once.**

If that is right, the severe band is not a point on one axis. It is the corner of two.

    ./bench/confusable.py [--top 20]
"""
import argparse, collections, json, math, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import probe
from retrieve import BM25, Dense, tokens


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--top", type=int, default=20)
    a = ap.parse_args()

    texts, area, raw = probe.corpus_texts()
    man = json.loads((ROOT / "manifest.json").read_text())
    dn = Dense()
    vec = {i: dn.cache[dn.cache_key(t)] for i, t in texts.items()
           if dn.cache_key(t) in dn.cache}
    print(f"  {len(vec)} of {len(texts)} documents are in the embedding cache", file=sys.stderr)
    ids = sorted(vec)
    cos = lambda x, y: sum(p * q for p, q in zip(vec[x], vec[y]))

    # Nearest neighbour of every document, and whether it is a sibling in the same cluster.
    near = {}
    for i in ids:
        best, bs = None, -2.0
        for j in ids:
            if j == i: continue
            s = cos(i, j)
            if s > bs: best, bs = j, s
        near[i] = (best, bs)

    print("\n  how close the nearest other document is\n")
    buckets = collections.Counter()
    for i, (j, s) in near.items():
        buckets[round(math.floor(s * 20) / 20, 2)] += 1
    for b in sorted(buckets, reverse=True):
        print(f"    cos >= {b:.2f}   {buckets[b]:>4}  {'#' * (buckets[b] // 5)}")

    print("\n  the tightest pairs — where a question about the subject cannot pick a side\n")
    seen = set()
    rows = sorted(near.items(), key=lambda kv: -kv[1][1])
    shown = 0
    for i, (j, s) in rows:
        key = tuple(sorted((i, j)))
        if key in seen: continue
        seen.add(key)
        # Can BM25 still separate them? If their texts share almost every term, it cannot, and a
        # question about either is unanswerable by retrieval of any kind. If they differ on a
        # qualifier, BM25 is the only thing keeping the pair apart — and a paraphrase removes it.
        ti, tj = set(tokens(texts[i])), set(tokens(texts[j]))
        jac = len(ti & tj) / len(ti | tj) if (ti | tj) else 0
        same = man.get(i, {}).get("cluster") == man.get(j, {}).get("cluster")
        print(f"    cos {s:.4f}  jaccard {jac:.2f}  {'same cluster' if same else 'ACROSS clusters'}")
        print(f"        {i}")
        print(f"        {j}")
        shown += 1
        if shown >= a.top: break

    # Per cluster, so the next round knows where to aim.
    cl = collections.defaultdict(list)
    for i in ids:
        c = man.get(i, {}).get("cluster")
        if c and not man.get(i, {}).get("section"): cl[c].append(i)
    stats = []
    for c, v in cl.items():
        if len(v) < 6: continue
        pairs = [cos(x, y) for n, x in enumerate(v) for y in v[n + 1:]]
        inner = sum(pairs) / len(pairs)
        tightest = max(pairs)
        # The margin that matters: the gap between a document's nearest sibling and the nearest
        # thing outside the cluster. A tight cluster in a sparse neighbourhood is easy to route to
        # and hard to resolve inside — which is exactly the case routing is supposed to win.
        stats.append((inner, tightest, len(v), c))
    print(f"\n  clusters of 6+, by how tightly packed they are  (targets for the qualifier lever)\n")
    print("     mean cos   max cos    n   cluster")
    for inner, tightest, n, c in sorted(stats, reverse=True)[:a.top]:
        print(f"      {inner:.3f}     {tightest:.3f}   {n:>3}   {c}")

    print(f"\n  and the loosest, as a control\n")
    for inner, tightest, n, c in sorted(stats)[:5]:
        print(f"      {inner:.3f}     {tightest:.3f}   {n:>3}   {c}")


if __name__ == "__main__":
    main()
