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

## Known defects in this fingerprint, carried deliberately

These were found by walking agents on `a84ac6cf463a1a6d` and are **not** fixed in it. Fixing a
corpus mid-campaign is the mistake this whole file exists to prevent: the routing arm would then
have run on one corpus and the retrieval census on another, which has already happened once. They
are written down here, they are the work list for the next fingerprint, and each has a `mapcheck`
rule attached so it cannot come back silently.

**D1 — a forwarding note that knows only two eras.** `hard-moved-overtime` sits in `payroll` and
says the rule there is "correct only before 2026-01-01". It is not: that page is the *oldest* of
three versions and was superseded on 2024-07-01, eighteen months before the move it describes. An
agent that trusts the note and stops answers a 2025 claim from the 2023 rule. Found by `t-overtime-04`,
independently again by `t-overtime-08`. The same shape applies to every `hard-moved-*` note.
→ **mapcheck R6**: a forwarding note must name every version of the subject, not only the two either
side of the move.

**D2 — a path that bypasses the revision notice.** `purchase-request → approval-threshold` reaches
the subject without passing anything that says it has been rewritten. Every other path passes a
revision notice; this one does not, so whether the walk is warned is a property of which row it
picked.
→ **mapcheck R7**: every path to a subject with more than one version passes a revision notice.

**D3 — two band vocabularies and no cross-walk.** `hard-perdiem-v2` gives lodging caps over bands
`B1`–`B4` and says the meal allowance and receipt threshold "followed the overseas allowance and
exchange rate rule unchanged". That older rule, `overseas-rates`, is banded `A`/`B`/`C`. Nothing in
the corpus maps one onto the other, so a v2-era question that needs a meal figure is unanswerable
on the evidence — correctly reported as such rather than guessed. Found by `t-perdiem-08`.
→ **mapcheck R8**: a document that defers to another for part of its answer must be in the same
qualifier vocabulary as the document it defers to, or carry the mapping.

D1 and D2 affect what a walk is warned about, not what the answer key says, and both were walked
past successfully — they cost calls, not hits. D3 is a genuine gap in the material: there is a
question shape the corpus cannot answer, and the honest outcome for it is "not found".
