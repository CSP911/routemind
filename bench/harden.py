#!/usr/bin/env python3
"""Push a question until plain RAG cannot find its answer — then check it is still a real question.

`probe.py` found the one lever that moves: wording. At A=3 fusion recall@10 is 0.39 against 1.00 at
A=0, while the three document-side factors are flat across their whole range. This takes that lever
and pushes it, one seed question at a time, until the answer falls out of the fused candidates
entirely.

**The search is free.** The reranker only reorders the fused top-20, so a gold document that is not
in the fused top-20 cannot be in B1's top-10 — the miss is proved without a rerank call. Fusion rank
costs one question embedding, so a round of eight variants costs less than a cent and no LLM call
beyond the one that writes them.

    ./bench/harden.py search [--rounds 4] [--variants 8] [--seeds 40]
    ./bench/harden.py verify        answerable? uniquely?  (the expensive half, and the honest one)
    ./bench/harden.py rerank        B1 proper, on what survived
    ./bench/harden.py emit          a gold-set fragment of what survived both

**Why the verification is not optional.** An adversarial search with no constraint converges on
questions so vague that nothing could match them — a break that is manufactured, not found, and
worse than no result at all. So every survivor is checked twice, by a model that never sees the
search:

    answerable   given the question and the gold document alone, quote the passage that answers it
    unique       given the question and the documents that outranked the gold, does any of them
                 answer it? If one does, this is a mislabelled question, not a hard one

A seed that fails either check is dropped and recorded as dropped. The count of what was thrown away
is part of the result: a search that has to discard most of what it makes is a search that was
optimising for the wrong thing.

**The adversarial move, and why it is legitimate.** The writer is shown the documents currently
outranking the gold and told it may lean into the vocabulary they share — that is exactly what a
person asking in their own words does, and it is what breaks a lexical retriever. It is only cheating
if the question stops being uniquely answerable by the gold, which is the second check's whole job.
"""
import argparse, json, os, pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import probe
from retrieve import Hybrid
from rerank import LLMReranker

STATE = ROOT / "harden-state.json"
VERIFY_MODEL = os.environ.get("PROBE_VERIFY_MODEL", "gpt-5")

WRITER = (
 "You rewrite a question so that a keyword-and-embedding search engine will fail to find its answer, "
 "while a person reading the answer document would still say the question is answered there.\n\n"
 "You are given the ANSWER document, the question as it currently stands, and the DECOYS — the "
 "documents the search engine is currently returning instead.\n\n"
 "Every rewrite must keep these true:\n"
 "- The answer is the same specific fact, and it is in the ANSWER document. Do not generalise the "
 "question until it has no single answer. Do not ask about something the document does not say.\n"
 "- No other document could answer it. In particular, none of the DECOYS may answer it.\n"
 "- It reads as one natural sentence a real person would type.\n\n"
 "What to change:\n"
 "- Use none of the ANSWER document's distinctive vocabulary. Replace its terms with the ordinary "
 "words somebody would use who has the problem but has never read this system's documents.\n"
 "- You may lean into the wording the DECOYS share, because that is what a person thinking about "
 "this general subject would say — as long as the question still has exactly one answer.\n"
 "- Describe the situation rather than naming it. Say the circumstance, not the policy's title.\n\n"
 "Reply with JSON only: {\"variants\": [\"...\", \"...\"]}")

ANSWERABLE = (
 "You are checking whether a document answers a question.\n\n"
 "Reply with JSON only: {\"answered\": true|false, \"quote\": \"the sentence from the document that "
 "answers it, verbatim, or empty\"}\n\n"
 "`answered` is true only if the document states the answer. It is false if the document is merely "
 "about the same subject, and false if answering would need a fact the document does not contain.")

UNIQUE = (
 "You are checking whether a question has more than one answer in a corpus.\n\n"
 "You are given a question and several candidate documents. Reply with JSON only: "
 "{\"answered_by\": [<candidate numbers that state an answer to the question>]}\n\n"
 "Include a candidate only if it actually states an answer. Being about the same subject is not "
 "enough. An empty list is the expected reply.")


def jparse(txt):
    m = re.search(r"\{.*\}", txt or "", re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except json.JSONDecodeError: return None


def seeds_from_probes(texts, n):
    """The hardest things already measured, worst first: a search starts where the map ran out."""
    out = []
    pr = ROOT / "probe-results.json"
    if pr.exists():
        for r in json.loads(pr.read_text()):
            if r["A"] < 2: continue
            rank = r.get("b1_rank") or r.get("fusion_rank")
            out.append({"id": f"p:{r['doc']}:{r['rung']}", "gold": [r["doc"]], "q": r["q"],
                        "start_rank": rank if rank else 999, "kind": "lexical"})
    p2 = ROOT / "probe2-results.json"
    if p2.exists():
        for r in json.loads(p2.read_text()):
            if r["rung"] != 3: continue
            ranks = [v for v in (r.get("b1") or r["fusion"]).values()]
            worst = max((v if v else 999) for v in ranks)
            out.append({"id": f"q:{r['key']}:{r['rung']}", "gold": r["gold"], "q": r["q"],
                        "start_rank": worst, "kind": r["kind"]})
    out.sort(key=lambda s: -s["start_rank"])
    return out[:n]


def worst_rank(h, q, gold, n=50):
    """How badly the retriever does on this question: the rank of the *last* gold document.

    The last, not the first, because a question needing two documents is only answered when both are
    in hand — and 999 stands for "not in the fused 50 at all", which is a miss the reranker cannot
    undo.
    """
    fused = h.search(q, n=n)
    ranks = [(fused.index(d) + 1 if d in fused else 999) for d in gold]
    return max(ranks), fused


def cmd_search(a):
    probe.guard()
    texts, area, raw = probe.corpus_texts()
    h = Hybrid(texts).warm()
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    seeds = seeds_from_probes(texts, a.seeds)
    print(f"  {len(seeds)} seeds · {a.rounds} rounds x {a.variants} variants", file=sys.stderr)

    for n, s in enumerate(seeds, 1):
        if s["id"] in state and state[s["id"]].get("rounds_done", 0) >= a.rounds: continue
        cur = state.get(s["id"]) or {"id": s["id"], "gold": s["gold"], "kind": s["kind"],
                                     "q": s["q"], "rank": None, "history": [], "rounds_done": 0}
        if cur["rank"] is None:
            cur["rank"], fused = worst_rank(h, cur["q"], cur["gold"])
        for rnd in range(cur["rounds_done"], a.rounds):
            _, fused = worst_rank(h, cur["q"], cur["gold"])
            decoys = [d for d in fused[:6] if d not in cur["gold"]][:5]
            body = ("ANSWER document:\n\n" + "\n\n".join(raw[d][:4000] for d in cur["gold"]) +
                    "\n\nCurrent question:\n\n" + cur["q"] +
                    "\n\nDECOYS — what the search returns instead:\n\n" +
                    "\n\n".join(f"[{i+1}] " + raw[d][:700] for i, d in enumerate(decoys)) +
                    f"\n\nWrite {a.variants} rewrites.")
            out = jparse(probe.ask(body, system=WRITER))
            variants = (out or {}).get("variants") or []
            if not variants:
                print(f"    {s['id']}: writer returned nothing, stopping this seed", file=sys.stderr)
                break
            scored = []
            for v in variants:
                if not isinstance(v, str) or len(v) < 15: continue
                r, _ = worst_rank(h, v, cur["gold"])
                scored.append((r, v))
            if not scored: break
            scored.sort(reverse=True)
            best_r, best_q = scored[0]
            cur["history"].append({"round": rnd + 1, "rank": best_r, "q": best_q,
                                   "tried": len(scored), "decoys": decoys})
            # Keep a rewrite only when it is genuinely worse for the retriever. Equal is not worse:
            # accepting ties lets the search drift through neutral rewrites and end up somewhere
            # that is different rather than harder.
            if best_r > cur["rank"]:
                cur["q"], cur["rank"] = best_q, best_r
            cur["rounds_done"] = rnd + 1
            state[s["id"]] = cur
            STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
            if cur["rank"] >= 999: break        # already out of the fused 50; nothing left to win
        print(f"    {n}/{len(seeds)}  {s['id']}  {s['start_rank']} -> {cur['rank']}", file=sys.stderr)
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")


def cmd_verify(a):
    texts, area, raw = probe.corpus_texts()
    h = Hybrid(texts).warm()
    state = json.loads(STATE.read_text())
    for k, c in sorted(state.items()):
        if "verdict" in c and not a.again: continue
        ans = jparse(probe.openai(
            "Question:\n\n" + c["q"] + "\n\nDocument:\n\n" +
            "\n\n".join(raw[d][:6000] for d in c["gold"]),
            model=VERIFY_MODEL, system=ANSWERABLE))
        _, fused = worst_rank(h, c["q"], c["gold"])
        above = [d for d in fused[:10] if d not in c["gold"]][:6]
        uni = jparse(probe.openai(
            "Question:\n\n" + c["q"] + "\n\nCandidates:\n\n" +
            "\n\n".join(f"[{i+1}] " + raw[d][:1800] for i, d in enumerate(above)),
            model=VERIFY_MODEL, system=UNIQUE))
        answered = bool((ans or {}).get("answered"))
        others = [above[i - 1] for i in ((uni or {}).get("answered_by") or [])
                  if isinstance(i, int) and 1 <= i <= len(above)]
        c["verdict"] = {"answerable": answered, "quote": (ans or {}).get("quote", "")[:300],
                        "also_answered_by": others, "ok": answered and not others}
        state[k] = c
        STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    {k}  answerable={answered}  others={len(others)}", file=sys.stderr)


def cmd_rerank(a):
    probe.guard()
    texts, area, raw = probe.corpus_texts()
    h = Hybrid(texts).warm()
    rr = LLMReranker()
    state = json.loads(STATE.read_text())
    for k, c in sorted(state.items()):
        if not (c.get("verdict") or {}).get("ok"): continue
        if "b1" in c and not a.again: continue
        fused = h.search(c["q"], n=50)
        ranked = rr.rank(c["q"], fused[:20], texts) + fused[20:]
        c["b1"] = {d: (ranked.index(d) + 1 if d in ranked else None) for d in c["gold"]}
        c["b1_hit10"] = all(v and v <= 10 for v in c["b1"].values())
        state[k] = c
        STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    {k}  B1 {c['b1']}  hit@10={c['b1_hit10']}", file=sys.stderr)


def cmd_report(a):
    state = json.loads(STATE.read_text())
    v = [c for c in state.values() if "verdict" in c]
    ok = [c for c in v if c["verdict"]["ok"]]
    scored = [c for c in ok if "b1" in c]
    print(f"\n  {len(state)} seeds searched · {len(v)} verified · {len(ok)} survived both checks")
    if v:
        print(f"    dropped: {sum(not c['verdict']['answerable'] for c in v)} not answerable · "
              f"{sum(bool(c['verdict']['also_answered_by']) for c in v)} answered elsewhere")
    if state:
        import statistics
        st = [c for c in state.values() if c.get("rank")]
        print(f"\n  fusion rank of the last gold document (999 = not in the fused 50)")
        print(f"    out of the fused 20 entirely: {sum(c['rank'] > 20 for c in st)}/{len(st)}"
              f"   — these break B1 whatever the reranker does")
        print(f"    median {statistics.median(c['rank'] for c in st):.0f}")
    if scored:
        print(f"\n  B1 hit@10 on the {len(scored)} that survived: "
              f"{sum(c['b1_hit10'] for c in scored)/len(scored):.2f}")
        for c in sorted(scored, key=lambda c: -c["rank"])[:12]:
            print(f"    {'MISS' if not c['b1_hit10'] else 'hit '}  rank {c['rank']:>3}  {c['q'][:96]}")


def cmd_emit(a):
    state = json.loads(STATE.read_text())
    texts, area, raw = probe.corpus_texts()
    out = []
    for n, (k, c) in enumerate(sorted(state.items()), 1):
        if not (c.get("verdict") or {}).get("ok"): continue
        if a.only_broken and c.get("b1_hit10"): continue
        out.append({"id": f"x{n}", "q": c["q"], "A_true": sorted({area[d] for d in c["gold"]}),
                    "D_true": c["gold"], "needs": "all" if len(c["gold"]) > 1 else "any",
                    "intent_A": 3, "intent_B": 3 if len({area[d] for d in c["gold"]}) > 1 else 0,
                    "source": k, "fusion_rank": c["rank"], "b1": c.get("b1")})
    print(yaml.safe_dump({"questions": out}, allow_unicode=True, sort_keys=False, width=100))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--rounds", type=int, default=4); s.add_argument("--variants", type=int, default=8)
    s.add_argument("--seeds", type=int, default=40)
    v = sub.add_parser("verify"); v.add_argument("--again", action="store_true")
    r = sub.add_parser("rerank"); r.add_argument("--again", action="store_true")
    sub.add_parser("report")
    e = sub.add_parser("emit"); e.add_argument("--only-broken", action="store_true")
    a = ap.parse_args()
    {"search": cmd_search, "verify": cmd_verify, "rerank": cmd_rerank,
     "report": cmd_report, "emit": cmd_emit}[a.cmd](a)
