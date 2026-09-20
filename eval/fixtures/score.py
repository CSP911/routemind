#!/usr/bin/env python3
"""Q5a — score a continuity fixture. Stage 1: retrieval only, no generation.

`eval/fixtures/README.md` is the contract this implements, and it promises contributors two numbers
kept apart, because conflating them is the whole reason fixtures exist:

    found       is the operative document in the top-k at all
    operative   is it ranked **above its own distractors**

A system can score 1.00 on the first and 0.00 on the second. That is not a retrieval failure — every
document was found, all of them are true and relevant — it is a failure to distinguish *found the
material* from *established which material is operative*. Raised by GovKM on 2026-09-18 as F5, and
written into `eval/PREREGISTRATION.md` §Q5a as: "a reranker blind to dates has no reason to put July
above March."

    ./eval/fixtures/score.py eval/fixtures/supplier-selection.yaml
    ./eval/fixtures/score.py eval/fixtures/*.yaml --out eval/runs/2026-09-21-q5a.json

**The fixture's documents go into the retrieval pool; its `truth` and `questions` never do.** That is
rule 2 of the contract, and here it is mechanical rather than a promise: `pool()` reads `documents`
only, and the scorer reads `truth` only after the search has returned.

**The corpus is not modified.** The fixture is merged into the pool in memory. Writing four documents
into `bench/corpus/` would change the fingerprint every run record is stamped with, which is a high
price for a test that does not need it.

Q5 is specified to run first against `git tag baseline-pre-continuity` — the implementation before
any state, age or supersession field exists — so that a later continuity-aware change is a delta from
a preserved result rather than a test designed around the fix. The contributor asked for exactly that.

**That instruction cannot be followed literally, and saying so is part of honouring it.** The tag is
from 2026-09-18 19:07 and has no `bench/` directory at all: the retrieval harness was built after it,
so there is nothing at that commit to run a fixture through. What the tag actually marks is the
*service* before any continuity field. The intent is therefore checked mechanically at every run —
`baseline()` below diffs `ontology/service/` between the tag and HEAD and refuses to record a result
as baseline if anything there has changed. Today that diff is empty, so a run at HEAD *is* a baseline
run; the day it stops being empty, this stops claiming otherwise on its own.
"""
import argparse, json, os, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bench"))
if os.environ.get("BENCH_PYLIB"):
    sys.path.insert(0, os.environ["BENCH_PYLIB"])
import yaml
import run as runner
from retrieve import Hybrid
from rerank import LLMReranker


def pool(fixtures):
    """The corpus plus every fixture's documents. `truth` and `questions` are not read here."""
    texts, area, one_liner, children, has_body = runner.corpus()
    added = {}
    for fx in fixtures:
        for d in fx["documents"]:
            if d["id"] in texts:
                sys.exit(f"  {fx['id']}: document id {d['id']} already exists in the corpus")
            # Indexed exactly the way run.py indexes a corpus document, or the fixture would be
            # competing on a different footing from everything it is ranked against.
            texts[d["id"]] = f"{d.get('name','')}. {d.get('one_liner','')}\n\n{d['body'].strip()}"
            added[d["id"]] = fx["id"]
    return texts, added


BASE_TAG = "baseline-pre-continuity"


def baseline():
    """Is this still the implementation the fixtures are supposed to measure first?

    Not a promise in prose — a diff. If `ontology/service/` has changed since the tag, something
    continuity-aware may have been added and a result recorded here is no longer a baseline result.
    """
    r = subprocess.run(["git", "diff", "--stat", BASE_TAG, "HEAD", "--", "ontology/service/"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return False, f"cannot compare against {BASE_TAG}: {r.stderr.strip()[:80]}"
    changed = r.stdout.strip()
    if changed:
        return False, f"ontology/service/ has changed since {BASE_TAG}:\n{changed}"
    return True, f"ontology/service/ is unchanged since {BASE_TAG}"


def rank_of(ids, doc):
    return ids.index(doc) + 1 if doc in ids else None


def score_question(q, ids, k):
    """Two numbers, kept apart. `found` is about the pool; `operative` is about the order."""
    op = q["operative"]
    r_op = rank_of(ids, op)
    found = r_op is not None and r_op <= k
    ranks = {d: rank_of(ids, d) for d in q.get("distractors") or []}
    # A distractor that was not retrieved cannot outrank anything, so it does not count against the
    # operative document. Treating "absent" as "beaten" is the reading that flatters the system; it
    # is also the correct one — the question is whether a wrong document was *preferred*.
    above = [d for d, r in ranks.items() if r is not None and r_op is not None and r < r_op]
    beats = found and not above
    return dict(q=q["q"], operative=op, rank=r_op, found=found,
                distractor_ranks=ranks, outranked_by=above, beats_distractors=beats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fixtures", nargs="+")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--n", type=int, default=20, help="candidates fused before any reranking")
    ap.add_argument("--no-rerank", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()

    fixtures = [yaml.safe_load(pathlib.Path(f).read_text(encoding="utf-8")) for f in a.fixtures]
    texts, added = pool(fixtures)
    print(f"  {len(texts)} documents ({len(added)} from {len(fixtures)} fixture(s)) · k={a.k}",
          file=sys.stderr)

    tag = subprocess.run(["git", "describe", "--tags", "--always"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    is_base, why = baseline()
    print(f"  baseline: {'yes' if is_base else 'NO'} — {why}", file=sys.stderr)
    h = Hybrid(texts).warm()
    rr = None if a.no_rerank else LLMReranker()

    out, rows = [], []
    for fx in fixtures:
        for q in fx["questions"]:
            ids = h.search(q["q"], n=a.n)          # fused candidates, best-first
            rows.append(("rag", fx["id"], score_question(q, ids, a.k)))
            if rr:
                rows.append(("rag+rerank", fx["id"],
                             score_question(q, rr.rank(q["q"], ids, texts), a.k)))

    print()
    for arm in ["rag", "rag+rerank"]:
        rs = [r for a_, _, r in rows if a_ == arm]
        if not rs: continue
        f = sum(r["found"] for r in rs) / len(rs)
        b = sum(r["beats_distractors"] for r in rs) / len(rs)
        print(f"  {arm:<12} found {f:.3f}   operative {b:.3f}   n={len(rs)}")
    print()
    for arm, fid, r in rows:
        mark = "ok  " if r["beats_distractors"] else ("ORDER" if r["found"] else "MISS ")
        print(f"  {mark} {arm:<12} rank {str(r['rank']):>4}   {r['q'][:58]}")
        if r["outranked_by"]:
            for d in r["outranked_by"]:
                print(f"         outranked by {d} at {r['distractor_ranks'][d]}")

    out = {"tag": tag, "k": a.k, "n": a.n,
           "fixtures": [f["id"] for f in fixtures],
           "contributed_by": [f.get("contributed_by") for f in fixtures],
           "documents_in_pool": len(texts), "from_fixtures": added,
           "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "results": [dict(arm=a_, fixture=fid, **r) for a_, fid, r in rows]}
    if a.out:
        p = ROOT / a.out
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  -> {a.out}")


if __name__ == "__main__":
    main()
