# Frozen for measurement — 2026-09-20

Nothing below this line is measured against anything else. The corpus changed seven times in a day,
twice in ways a diff of the generator would not have shown, and six runs were discarded for it. This
is the line.

## What is frozen

| | |
|---|---|
| corpus fingerprint | **`a84ac6cf463a1a6d`** over 1,126 retrievable documents |
| generator | `bench/crowd.py write --grid 4x4x4` — the extension is not in version control because it is regenerated from that file in seconds; the fingerprint is what makes "the same corpus" checkable |
| base corpus | `bench/corpus`, 779 retrievable, untouched since it was generated |
| routing table | `bench/use_when_maintained.yaml`. `bench/spec.yaml`'s frozen sentences are kept and **fail** the precondition by four |
| gold | `eval/gold/hard.yaml` 640 · `eval/gold/hard-temporal.yaml` 60 |
| models | embeddings `text-embedding-3-large` · reranker `gpt-5` · routing agents run through Claude Code against the real MCP surface |

Check it before any run:

    ./bench/crowd.py fingerprint                    ->  1126 documents  sha256 a84ac6cf463a1a6d
    BENCH_USE_WHEN=maintained ./bench/mapcheck.py   ->  passes
    ./bench/audit.py eval/gold/hard.yaml            ->  360 clean, 280 shortlisted (judged in gold/AUDIT.md)

A different fingerprint means a different corpus and a different campaign. Results are not pooled
across fingerprints, and no run record is written without one in it.

## What this supersedes

Every measurement taken before today is against an earlier corpus and is **not comparable**. In
particular the 640-question baseline run: the retrieval pool went 1,114 → 1,126, and 330 documents
changed text — all 320 rows among them, because the provenance line now names the middle version.
The direction of the change is guessable (the added notices carry a person's vocabulary, so they
compete for the top ten on exactly the questions where the rows cannot) and the size is not. It is
re-run rather than reused.

Kept as record, not as result: `eval/runs/` from 2026-09-19 and earlier.

## The arms

Named for what they are. Two comparisons are controlled, one is realistic.

|  | on its own | with its own second stage |
|---|---|---|
| retrieval | `rag` | `rag+rerank` |
| routing | `routing` | `routing+overlay` |

    rag              vs routing            both bare. The controlled comparison
    rag+rerank       vs routing+overlay    each with what its designers would add. The realistic one
    rag+rerank       vs routing            the sceptic's build against routing alone — the hardest ask

The `+` column is **not** one variable applied to both sides. A reranker is what a retrieval engineer
adds; a working set is what RouteMind has. Calling that a factorial would be wrong, so the bare row
carries the controlled claim and the `+` row carries the realistic one, and the report says which is
which every time.

`routing-scoped` — retrieval inside the subtree a walk opened — stays as a diagnostic. It answers
"was the gain the reading, or a smaller haystack?" and is never a row of the main table.

## Census and sample, which are not the same thing

**The retrieval arms are a census.** 700 questions, every one, deterministic given the fingerprint.
No sampling error; the number is the number.

**The routing arms are a sample.** Each walk is a fresh agent against the real MCP surface, at about
48k session tokens, so 50 questions go through rather than 700 — stratified by family and lever.
Intervals attach to these and not to the others, and a routing figure is never quoted beside a
retrieval figure without the n.

## What is recorded per run

    the fingerprint · the git tag · mapcheck result · which hop 0 · every model by name
    per question: the arm, the hit, the rank, the document the answer came from
    for routing: the agent's report **verbatim** — every command in order, and its notes

The notes are data. On the first six walks a fresh reader found two things the desk audit had missed
— a second "receipt threshold" of a different kind sitting in the same area, and a delegation limit
of 450 thousand KRW on a twelve-million-won purchase. Neither would have survived being summarised.

## Known defects in this fingerprint — one real, two of them my mistake

Written from the n=50 sample as three defects. Then R6 was implemented and the 700-question census
ran, and two of the three turned out not to be defects at all. Both errors were mine and both are
the same error: **reading the corpus doing what it was built to do and calling it broken.**

### D1 — a forwarding note that knows only two eras. Real, and it costs hits.

`hard-moved-overtime` sits in `payroll` and says overtime premiums moved to attendance on
2026-01-01, and that the payroll page is correct before then. It is not: that page is the *oldest*
of three versions and was superseded on 2024-07-01, eighteen months before the move it describes.
`hard-moved-threshold` has the same shape.

**Observed, not predicted.** On the 700-question census a walk read the note, did exactly what it
said, and answered a 2025 claim from the 2023 rule. It is the only miss in 700. The paragraph that
used to sit here said D1 "costs calls, not hits", on the evidence of fifty walks that had happened
to go the other way — a statement about a sample presented as a property of the defect.

→ **`mapcheck` R6**, implemented: a forwarding note must name every date its subject's own revision
legend names, not only the date it moved. Both notes fail it, both are silent about 2024-07-01.
Carried in this fingerprint with `./bench/mapcheck.py --carry R6`, which prints them as CARRIED and
has to be typed every run. Fixed in the next fingerprint.

### D2 — "a path that bypasses the revision notice". Not a defect. Designed.

Recorded as: `purchase-request → approval-threshold` reaches the subject without passing anything
saying it has been rewritten. True — and true of every path to every superseded document, because
`bench/crowd.py:479` says so on purpose: *"None of them were withdrawn, and the oldest says nothing
at all about having been replaced."* That silence is the difficulty the `stale-old` questions are
made of. A rule requiring the old page to announce itself would delete the thing being measured.

The guarantee the design actually offers is R4 — the notice sits **at the area**, which every walk
sees at hop 0 before it descends anywhere. R4 passes. There is no R7 and there should not be one.

### D3 — "two band vocabularies and no cross-walk". Real, but I overstated it.

`hard-perdiem-v2` is banded `B1`–`B4` and defers the meal allowance to `overseas-rates`, which is
banded `A`/`B`/`C`. I wrote that this made a question shape *unanswerable*. It does not:
`hard-perdiem-legend-band` maps Tokyo→B1, Singapore→B2, Jakarta→B3, Dhaka→B4, and `overseas-rates`
bands by region, so B2 → Singapore → South-East Asia → Band B resolves in two hops.

What is true is narrower and worth keeping: the two hops are never stated as a route, and a careful
reader declines to invent one — which is what the walk on `t-perdiem-08` did, correctly, flagging it
rather than guessing. That is a documentation gap, not a hole in the material, and no rule enforces
a thing a good reader already handles by refusing.

### What this episode is

Three defects recorded from a sample; one survived contact with a census and a check. The two that
did not were both cases of me treating a designed property as a fault, and neither would have been
caught by looking harder at the sample — one needed 700 walks, the other needed reading the
generator. The run records for this fingerprint say `mapcheck R1–R5 pass`, which was accurate when
they were written; R6 did not exist yet, and where it matters the census result says what happened.
