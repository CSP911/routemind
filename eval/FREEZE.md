# Frozen for measurement — 2026-09-20

Nothing below this line is measured against anything else. The corpus changed seven times in a day,
twice in ways a diff of the generator would not have shown, and six runs were discarded for it. This
is the line.

## What is frozen

| | |
|---|---|
| corpus fingerprint | **`7dfd5538de294fcb`** over 1,126 retrievable documents |
| generator | `bench/crowd.py write --grid 4x4x4` — the extension is not in version control because it is regenerated from that file in seconds; the fingerprint is what makes "the same corpus" checkable |
| base corpus | `bench/corpus`, 779 retrievable, untouched since it was generated |
| routing table | `bench/use_when_maintained.yaml`. `bench/spec.yaml`'s frozen sentences are kept and **fail** the precondition by four |
| gold | `eval/gold/hard.yaml` 640 · `eval/gold/hard-temporal.yaml` 60 |
| models | embeddings `text-embedding-3-large` · reranker `gpt-5` · routing agents run through Claude Code against the real MCP surface |

Check it before any run:

    ./bench/crowd.py fingerprint                    ->  1126 documents  sha256 7dfd5538de294fcb
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
