#!/usr/bin/env python3
"""Is each question answerable, and does it name its answer? A desk check, before anything runs.

Six runs were discarded this week and four of them died of the same thing: the answer key was wrong,
and it was found by watching an arm fail. That is the expensive way round, and worse, it invites the
wrong diagnosis — a walk that wanders looks like a routing failure whether the map is bad or the
question is unanswerable as written.

The clearest case: *"For a trip in November 2025, did the day we flew home count as an allowance
day?"* with `overseas-rates` as the gold document. The question never says the trip was overseas. The
agent read `domestic-rates`, which is what a careful person would also do, and was scored as failing.

So the questions are checked at the desk, with no API and no arm:

    reachable   the gold document exists and hangs off an area, so a walk can arrive at it
    named       the question carries the words that pick this document out of its neighbours —
                the discriminating terms of its own id and title, or something that implies them
    unique      no other document answers as well. Approximated by BM25 over the whole corpus:
                anything outranking the gold on the question's own words is a candidate rival, and
                a rival that really answers is a labelling error rather than a hard question.

                **A rival that is another version of the same subject is not a flag.** Three versions
                of one rule are supposed to look alike and to outrank each other — that is the
                difficulty the time axis is made of, and flagging it would flag the design. What
                matters is an unrelated document that answers just as well.

BM25 needs no API, so this costs nothing and can run on every question before every campaign.

**It reports, it does not decide.** The last two checks end in a person reading the shortlist; what
the script does is make the shortlist small and put the evidence next to it. Nothing here looks at
which arm wins, and the flags are recorded so the judgement can be argued with.

    ./bench/audit.py eval/gold/hard-stale.yaml [--full]
"""
import argparse, json, os, re, sys
import yaml

ROOT = __import__("pathlib").Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gold"); ap.add_argument("--full", action="store_true")
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()
    os.environ.setdefault("BENCH_EXTRA_CORPUS", "bench/corpus-hard")
    import run as runner
    from retrieve import BM25, tokens

    texts, area, one, kids, has_body = runner.corpus()
    bm = BM25(texts)
    qs = yaml.safe_load(open(a.gold, encoding="utf-8"))["questions"]

    # Every node's ancestors, so "can a walk get here at all" is a fact rather than a hope.
    parent = {}
    for p, cs in kids.items():
        for c in cs: parent[c] = p
    def reachable(i):
        seen, cur = set(), i
        while cur in parent and cur not in seen:
            seen.add(cur); cur = parent[cur]
        return cur in runner.rows()

    # id -> the subject a document is a version of, so kinship is a fact rather than a guess.
    man = json.loads((ROOT / "crowd-manifest.json").read_text())
    versions = {}
    for i, m in man.items():
        if isinstance(m, dict) and m.get("family"): versions[i] = m["family"]
    import crowd
    for f in crowd.FAMILIES:
        for old, _ in f["supersedes"]: versions[old] = f["key"]

    flagged, ok = [], 0
    for q in qs:
        d = q["D_true"][0]
        ranked = [i for _, i in bm.search(q["q"])]
        rank = ranked.index(d) + 1 if d in ranked else None
        # Same-subject rivals are separated out: a superseded version, the table that replaced it,
        # or the notice between them is a near-duplicate on purpose.
        fam = versions.get(d)
        rivals = [i for i in ranked[:a.top] if i != d and versions.get(i) != fam]
        kin = [i for i in ranked[:a.top] if i != d and fam and versions.get(i) == fam]
        reach = reachable(d)
        # The question's own words against the gold document's distinguishing ones. A gold document
        # the question does not out-and-out name is not automatically broken — a legend may carry the
        # mapping — but it is the shortlist worth reading.
        qt, dt = set(tokens(q["q"])), set(tokens(one.get(d, "") + " " + d.replace("-", " ")))
        overlap = len(qt & dt)
        # Outside a retriever's reach at all, unreachable in the tree, or sharing no word with what
        # it is supposed to name. Rank alone is not a fault: a walk does not use BM25, and a prose
        # page among 1,100 documents can sit at 84 and still be the only right answer.
        # What is actually a fault: the walk cannot get there, no retriever could ever see it, the
        # question shares no word with what it names, or an *unrelated* document sits above it in the
        # top three and might answer just as well. A low rank on its own is not a fault — a walk does
        # not use BM25, and a prose page among 1,100 documents can sit at 84 and still be the only
        # right answer. Kin above it is the design, and is printed rather than flagged.
        bad = (not reach) or rank is None or overlap == 0 or bool(rivals[:3])
        if bad: flagged.append((q, d, rank, rivals, reach, overlap, kin))
        else: ok += 1

    print(f"\n  {a.gold} — {len(qs)} questions · {ok} clean · {len(flagged)} to read\n")
    for q, d, rank, rivals, reach, overlap, kin in flagged:
        print(f"  {q['id']}   gold {d}   BM25 rank {rank or '>50'}"
              f"{f'   kin above it: {len(kin)}' if kin else ''}"
              f"{'' if reach else '   NOT REACHABLE'}"
              f"{'   question shares no word with the gold title' if overlap == 0 else ''}")
        print(f"    Q  {q['q'][:150]}")
        print(f"    G  {one.get(d,'')[:120]}")
        for r in rivals[:a.top]:
            print(f"    ·  {r:<38} {one.get(r,'')[:88]}")
        print()
    if flagged:
        print(f"  Read these {len(flagged)} and decide for each: is the gold document the only right")
        print(f"  answer, and does the question say enough to pick it? Fix the question or the label,")
        print(f"  not the arm.\n")


if __name__ == "__main__":
    main()
