#!/usr/bin/env python3
"""Run the arms over a gold set and score them.

    ./bench/run.py eval/gold/pilot.yaml               both arms
    ./bench/run.py eval/gold/pilot.yaml --arm B1      one

**Four arms, and they are a 2x2: routing on or off, reranking on or off.** They are named for what
they are rather than by a letter, because a reader should not have to hold a key in their head to
know which line of a table is the baseline.

    rag               hybrid retrieval over the whole corpus. Top k. Nothing else.
    rag+rerank        the same, then an LLM reorders the 20 candidates. What a sceptic builds.
    routing           the agent walks the human-written tree — open a table, read a document, go
                      back — and answers from what it collected. No ranking step anywhere, which is
                      what the product actually does.
    routing+rerank    the same walk, then the reranker orders what it collected.

Three comparisons come out of it, and the middle one is the one that matters:

    rag        vs routing          what routing is worth with the reranker taken off both sides
    rag+rerank vs routing          the sceptic's build against routing alone — routing gives up a
                                   component and still has to win. If it wins here the rest follows
    rag+rerank vs routing+rerank   the same component on both sides

`--arm routing-scoped` is a diagnostic rather than a fourth comparison: retrieval restricted to the
subtree the walk opened. It answers "was the gain the reading, or just a smaller haystack?" and is
reported beside the walk, never as a row of the main table.

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
    """hop 0. Frozen by default; `BENCH_USE_WHEN=maintained` selects the updated twin.

    The frozen sentences predate the extension and stay untouched, so a win cannot come from having
    rewritten the table for the test. The maintained ones are what an operator would have written
    after adding 345 documents and superseding five subjects, and running both is how the value of
    that maintenance gets a number instead of an assumption.
    """
    spec = yaml.safe_load((ROOT / "spec.yaml").read_text(encoding="utf-8"))
    frozen = {a: spec[a]["frozen_use_when"] for a in spec}
    if os.environ.get("BENCH_USE_WHEN") != "maintained":
        return frozen
    upd = yaml.safe_load((ROOT / "use_when_maintained.yaml").read_text(encoding="utf-8"))
    missing = set(frozen) - set(upd)
    if missing: sys.exit(f"  use_when_maintained.yaml is missing areas: {sorted(missing)}")
    return {a: " ".join(upd[a].split()) for a in frozen}


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
    ap.add_argument("--arm", action="append",
                    choices=["rag", "rag+rerank", "routing", "routing+overlay", "routing-scoped"],
                    help="repeatable; default runs all four")
    ap.add_argument("--out")
    # 0 is unbounded, and is the default: the pilot showed the cap, not the routing, was what the
    # severe band measured. --steps is a runaway stop, not a budget.
    ap.add_argument("--budget", type=int, default=0)
    ap.add_argument("--steps", type=int, default=30)
    # Only `routing-scoped` still consults this: which arm reranks is now decided by the arm's name.
    ap.add_argument("--no-rerank", action="store_true",
                    help="routing-scoped only: score it on fusion order, without a reranking call")
    ap.add_argument("--skip-hopeless", action="store_true",
                    help="do not spend a reranking call on a question whose answer is not among the "
                         "candidates; the miss is already decided")
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
    agent_ov = Agent(rows(), children, one_liner, has_body,
                     budget=a.budget or None, steps=a.steps, body=texts, overlay=True)
    # The single-decision router is gone from the default set. Its question — "is the gain the
    # table or just a smaller haystack?" — is answered more tightly by `routing-scoped`, which
    # retrieves over the exact subtree the walk opened rather than over two areas a separate call
    # named, so nothing varies but whether reading was allowed. `bench/route.py` stays in the tree.
    arms = a.arm or ["rag", "rag+rerank", "routing", "routing+overlay"]
    # Two walkers, because the working set changes how the walk goes rather than what is done with
    # it afterwards. The reranker could be bolted on after the fact; this cannot, so the two routing
    # arms each walk for themselves and `walks` is keyed by arm as well as question.
    walks = {}

    out = a.out or f"eval/runs/{time.strftime('%Y-%m-%d')}-pilot.json"
    outp = ROOT.parent / out
    outp.parent.mkdir(parents=True, exist_ok=True)

    def save():
        outp.write_text(json.dumps({"k": a.k, "per_hop": a.per_hop, "budget": a.budget,
                                    "steps": a.steps, "gold": a.gold,
                                    "no_rerank": bool(a.no_rerank),
                                    "router_model": router.model, "rerank_model": rr.model,
                                    "embed_model": h.dense.model, "results": results},
                                   indent=1, ensure_ascii=False), encoding="utf-8")

    results = []
    for arm in arms:
        use_routing = arm.startswith("routing")
        use_rerank = arm == "rag+rerank"
        for n, q in enumerate(g, 1):
            picked, raw, hops, walk, hopeless = None, "", None, None, False
            if use_routing:
                ag = agent_ov if arm == "routing+overlay" else agent
                key = (arm if arm != "routing-scoped" else "routing", q["id"])
                if key not in walks:
                    before = dict(ag.usage)
                    w = ag.walk(q["q"])
                    w["usage"] = {k: ag.usage[k] - before[k] for k in ag.usage}
                    walks[key] = w
                walk = walks[key]
                hops = walk["hops"]
                got = [i for i in walk["collected"] if i in texts]
                picked = sorted({area[i] for i in walk["visited"] if i in area})
                raw = " | ".join(walk["log"])[:400]
                if arm == "routing-scoped":
                    # The diagnostic: retrieval inside the subtree the walk opened, not what it read.
                    reach = subtree(walk["visited"], children, texts)
                    cand = h.search(q["q"], scope=reach or None, n=max(a.k, 20))
                    ranked = cand if a.no_rerank else rr.rank(q["q"], cand[:20], texts) + cand[20:]
                else:
                    # What the agent collected, in the order it collected it. Reranking a handful of
                    # documents and keeping the top k returns the same handful, so `routing` and
                    # `routing+rerank` can only differ once a walk collects more than k.
                    # No ranking step on either routing arm: the product walks, reads and answers.
                    # What separates them is how the walk went, not what happened to it afterwards.
                    ranked = got
            else:
                cand = h.search(q["q"], scope=None, n=max(a.k, 20))
                hopeless = a.skip_hopeless and use_rerank and not (set(q["D_true"]) & set(cand[:20]))
                ranked = cand if (not use_rerank or hopeless) else \
                         rr.rank(q["q"], cand[:20], texts) + cand[20:]
            r = score(q, ranked, area, picked, a.k)
            r["reranked"] = use_rerank and not hopeless
            if use_routing and arm != "routing-scoped":
                r["working_set"] = walk.get("working_set") or {}
                r["overlay_ops"] = len(walk.get("overlay_ops") or [])
            if use_routing:
                r["hops"] = hops
                r["read_n"] = len(got)
                r["returns"] = walk["returns"]; r["opens"] = walk["opens"]
                r["read_chars"] = walk["read_chars"]; r["usage"] = walk["usage"]
                r["exhausted"] = walk["exhausted"]
                r["read_exact"] = bool(use_rerank or len(got) <= a.k)
            r.update(arm=arm, id=q["id"], needs=q["needs"], picked=picked, router_said=raw,
                     hops=hops, collected=len(ranked),
                     top=[{"id": i, "area": area[i]} for i in ranked[:a.k]])
            results.append(r); save()
            extra = (f"  hops {r['hops']} read {r['read_chars']//1000}k"
                     f" tok {sum(r['usage'].values())//1000}k") if use_routing else ""
            print(f"    {arm:<15} {q['id']:<20} {'ok  ' if r['retrieval_hit'] else 'MISS'}"
                  f"  rank {str(r['rank'] or '-'):<4} routing {'ok ' if r['routing_hit'] else '-- '}"
                  f"{extra}", file=sys.stderr)

    save()
    print(f"\n  written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
