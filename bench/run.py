#!/usr/bin/env python3
"""Run the arms over a gold set and score them.

    ./bench/run.py eval/gold/pilot.yaml               both arms
    ./bench/run.py eval/gold/pilot.yaml --arm B1      one

Three arms:

    A1   the agent walks the tree — hop 0, open a table, read documents, go back if the answer is
         somewhere else — with a hop budget. What the system actually is.
    A3   the routing layer as a single decision: pick areas from hop 0 once, then hybrid + reranker
         inside them. The hierarchy is not descended. This is the ablation, not the design.
    B1   hybrid + reranker over the whole corpus, no routing at all.

A1 against A3 is what the tree is worth. A3 against B1 is what one routing decision is worth.

Everything except the routing layer is held identical: same corpus, same embeddings, same BM25, same
reranker, same k, and the same questions through both.

Scored apart, because a wrong hop 0 arriving as a retrieval miss is how a reranker gets tuned for a
problem the table caused:

    F1  routing    did the arm look in an area that contains an answer
    F2  retrieval  is a D_true document in the top k
    F3  rank       where the first one sits

B1 has no routing step. Its F1 is computed from where its top-k actually came from, which is the
closest honest analogue — it says whether an unrouted retriever ended up in the right area anyway.
"""
import argparse, json, os, pathlib, re, sys, time
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from retrieve import Hybrid
from rerank import LLMReranker
from route import Router
from agent import Agent
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def corpus():
    """Two views of the same tree: what is retrievable, and what is walkable.

    A section page is not an answer — it is a signpost this study added — so it is kept out of the
    retrieval pool. It *is* part of the tree the agent walks, because walking past signposts is the
    whole of what a hierarchy is for.
    """
    man = json.loads((ROOT / "manifest.json").read_text())
    roots = [ROOT / "corpus" / "regions"]
    # The 700 stay frozen. BENCH_EXTRA_CORPUS=bench/corpus-hard adds the qualifier families on top,
    # so 700 and 780 are two rows of one table instead of one number that changed meaning.
    extra = os.environ.get("BENCH_EXTRA_CORPUS")
    if extra:
        ex = pathlib.Path(extra)
        if not ex.is_absolute(): ex = ROOT.parent / ex
        roots.append(ex / "regions")
        cm = ex.parent / "crowd-manifest.json"
        if cm.exists(): man.update(json.loads(cm.read_text()))
    texts, area, one_liner, parent, has_body = {}, {}, {}, {}, {}
    for r in roots:
      for p in r.rglob("*.md"):
        m = FM.match(p.read_text(encoding="utf-8")); fm = yaml.safe_load(m.group(1)) or {}
        i = fm.get("id") or p.stem
        one_liner[i] = fm.get("one_liner", "")
        parent[i] = fm.get("parent") or p.parent.name
        has_body[i] = bool(m.group(2).strip())
        area[i] = p.parent.name
        if man.get(i, {}).get("section"): continue
        # `use_when` is deliberately not indexed. It is the routing table itself, and an arm that
        # runs without a table must not be fed it, or the comparison is over before it starts.
        texts[i] = f"{fm.get('name','')}. {fm.get('one_liner','')}\n\n{m.group(2).strip()}"
    children = {}
    for i, par in parent.items():
        if par and par != i: children.setdefault(par, []).append(i)
    # Sorted, because the order was whatever rglob returned — not reproducible across machines, and
    # the agent is shown this list verbatim. A benchmark whose prompt depends on directory order is
    # a benchmark that cannot be replicated.
    for k in children: children[k].sort()
    return texts, area, one_liner, children, has_body


def rows():
    spec = yaml.safe_load((ROOT / "spec.yaml").read_text(encoding="utf-8"))
    return {a: spec[a]["frozen_use_when"] for a in spec}


def subtree(visited, children, texts):
    """Every retrievable document under anything the walk opened.

    The walk's contribution is *where to look*; this is the set that follows from it. A node the
    agent opened contributes its whole subtree, because opening a section is a claim about the
    section, not about the one row that caught its eye.
    """
    out, seen = [], set()
    stack = list(visited)
    while stack:
        n = stack.pop()
        if n in seen: continue
        seen.add(n)
        if n in texts: out.append(n)
        stack += children.get(n, [])
    return out


def score(q, ranked, area, picked, k):
    d_true, a_true = set(q["D_true"]), set(q["A_true"])
    top = ranked[:k]
    looked = set(picked) if picked is not None else {area[i] for i in top}
    f1 = bool(a_true & looked) if q["needs"] == "any" else a_true <= looked
    hit = [n for n, i in enumerate(top, 1) if i in d_true]
    return {"routing_hit": f1,
            "areas_looked": sorted(looked),
            "area_precision": (len(a_true & looked) / len(looked)) if looked else 0.0,
            "retrieval_hit": bool(hit), "rank": hit[0] if hit else None,
            "mrr": (1.0 / hit[0]) if hit else 0.0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gold"); ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--per-hop", type=int, default=2)
    ap.add_argument("--arm", choices=["A1", "A3", "B1"]); ap.add_argument("--out")
    # 0 is unbounded, and is the default: the pilot showed the cap, not the routing, was what the
    # severe band measured. --steps is a runaway stop, not a budget.
    ap.add_argument("--budget", type=int, default=0)
    ap.add_argument("--steps", type=int, default=30)
    a = ap.parse_args()

    g = yaml.safe_load(pathlib.Path(a.gold).read_text(encoding="utf-8"))["questions"]
    texts, area, one_liner, children, has_body = corpus()
    print(f"  {len(texts)} retrievable · {len(one_liner)} in the tree · {len(g)} questions · "
          f"k={a.k} · areas/hop={a.per_hop} · "
          f"returns={'unbounded' if not a.budget else a.budget} · turn ceiling={a.steps}",
          file=sys.stderr)
    h = Hybrid(texts).warm()
    rr = LLMReranker()
    router = Router(rows(), per_hop=a.per_hop)
    # `texts` is what READ hands back — the same string the retrieval arms index, so the walker and
    # the retriever are reading the identical corpus and no arm sees a word the others cannot.
    agent = Agent(rows(), children, one_liner, has_body,
                  budget=a.budget or None, steps=a.steps, body=texts)
    arms = [a.arm] if a.arm else ["B1", "A3", "A1"]

    out = a.out or f"eval/runs/{time.strftime('%Y-%m-%d')}-pilot.json"
    outp = ROOT.parent / out
    outp.parent.mkdir(parents=True, exist_ok=True)

    def save():
        outp.write_text(json.dumps({"k": a.k, "per_hop": a.per_hop, "budget": a.budget,
                                    "steps": a.steps, "gold": a.gold,
                                    "router_model": router.model, "rerank_model": rr.model,
                                    "embed_model": h.dense.model, "results": results},
                                   indent=1, ensure_ascii=False), encoding="utf-8")

    results = []
    for arm in arms:
        for n, q in enumerate(g, 1):
            picked, raw, hops, walk = None, "", None, None
            if arm == "A1":
                # Scored two ways, because they answer different questions and comparing the first
                # against B1 is not a fair fight: the agent reads one or two documents, B1 returns
                # ten candidates, and "did it pick exactly right" is strictly harder than "was it in
                # the top ten".
                #
                #   read     what the agent actually collected. What a consumer is handed.
                #   scoped   retrieval inside the subtrees the walk opened, filled to k. Same unit
                #            as B1 and A3 — the walk chooses where, retrieval chooses what.
                walk = agent.walk(q["q"])
                hops = walk["hops"]
                got = [i for i in walk["collected"] if i in texts]
                read_ranked = rr.rank(q["q"], got, texts) if len(got) > 1 else got
                picked = sorted({area[i] for i in walk["visited"] if i in area})
                reach = subtree(walk["visited"], children, texts)
                cand = h.search(q["q"], scope=reach or None, n=max(a.k, 20))
                ranked = rr.rank(q["q"], cand[:20], texts) + cand[20:]
                raw = " | ".join(walk["log"])[:400]
            else:
                scope = None
                if arm == "A3":
                    picked, raw = router.pick(q["q"])
                    scope = [i for i in texts if area[i] in picked] or None
                cand = h.search(q["q"], scope=scope, n=max(a.k, 20))
                ranked = rr.rank(q["q"], cand[:20], texts) + cand[20:]
            r = score(q, ranked, area, picked, a.k)
            if arm == "A1":
                rd = score(q, read_ranked, area, picked, a.k)
                r["read_retrieval_hit"] = rd["retrieval_hit"]
                r["read_rank"] = rd["rank"]
                r["read_mrr"] = rd["mrr"]
                r["read_n"] = len(read_ranked)
                r["reach_n"] = len(reach)
                r["returns"] = walk["returns"]
                r["opens"] = walk["opens"]
                r["read_chars"] = walk["read_chars"]
                # A walk that hit the turn ceiling never said DONE. Its hop count is the ceiling
                # speaking, not the question, and the report has to be able to drop it.
                r["exhausted"] = walk["exhausted"]
            r.update(arm=arm, id=q["id"], needs=q["needs"], picked=picked, router_said=raw,
                     hops=hops, collected=len(read_ranked) if arm == "A1" else None,
                     top=[{"id": i, "area": area[i]} for i in ranked[:a.k]])
            results.append(r); save()
            extra = (f"  read {'ok ' if r['read_retrieval_hit'] else 'MISS'}({r['read_n']})"
                     f" scope {r['reach_n']:>3} back {r['returns']}"
                     f" read {r['read_chars']//1000}k"
                     f"{' EXHAUSTED' if r['exhausted'] else ''}") if arm == "A1" else ""
            print(f"    {arm} {q['id']:<4} routing {'ok ' if r['routing_hit'] else 'MISS'}"
                  f"  retrieval {'ok ' if r['retrieval_hit'] else 'MISS'}"
                  f"  rank {str(r['rank'] or '-'):<4}"
                  f"  hops {hops if hops is not None else '-'}{extra}"
                  f"  {','.join(picked) if picked else ''}", file=sys.stderr)

    save()
    print(f"\n  written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
