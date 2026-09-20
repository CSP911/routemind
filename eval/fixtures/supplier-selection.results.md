# supplier-selection-x — Q5a, first run

    2026-09-21 · baseline: ontology/service/ unchanged since baseline-pre-continuity
    783 documents in the pool (779 corpus + 4 fixture) · k=10 · fused n=20
    embed text-embedding-3-large · rerank gpt-5
    ./eval/fixtures/score.py eval/fixtures/supplier-selection.yaml

Contributed by **GovKM**. The contract promised results would be preserved beside the fixture once
they existed; this is that, and it is the first time the fixture has been scored.

| arm | found | operative | n |
|---|---|---|---|
| `rag` | 0.667 | 0.667 | 3 |
| `rag+rerank` | **1.000** | **1.000** | 3 |

## F5 happens, and it looks exactly as described

> *Can I place a new order for X with Supplier A?*

| | rank under `rag` |
|---|---|
| `x-supplier-a-approved` — the March approval, **withdrawn 7 July** | **6** |
| `x-supplier-b-approved` — the July decision, the operative one | **14** |

Read the top ten and you are told Supplier A is the registered source for X. That is a true document,
a relevant document, and a findable document, and the answer built from it is wrong. Nothing here is
a retrieval failure: fusion did what fusion does, and put the more topical page above the one that
replaced it. This is the distinction the fixture exists to make — *found the material* is not
*established which material is operative*.

## The prediction about the reranker did not hold

`eval/PREREGISTRATION.md` §Q5a says: *"a reranker blind to dates has no reason to put July above
March."* On this fixture it had one, and used it. The reranker moved the operative document from 14
to 2 and scored 1.000 on both measures.

The reason is in the fixture's own text. `x-supplier-b-approved` says, in prose:

> **This replaces the approval of Supplier A dated 3 March 2025**, which is withdrawn from the same date.

Rule 1 of the contract explicitly permits that — *"a document that says 'this supersedes the March
decision' in its prose is fine — people write that"* — and it is what a reader can act on and a
ranker cannot. So the finding is narrower and more useful than the prediction: **F5 bites the
ordering, and a reader that sees the supersession sentence escapes it.**

That locates the real exposure. A system answering from ranked passages without a reader is exposed.
A system that reads the top document and finds the sentence is not — *provided somebody wrote the
sentence*.

## What this run does not establish

**n=3.** Three questions, one fixture. Every figure above is three trials; 0.667 is "two of three".
No interval attaches to any of it and none is quoted.

**One history, and a well-documented one.** GovKM's scenario has an explicit supersession sentence
and clean dates. The harder case — nobody wrote the sentence, and currency has to be inferred from
dates alone — is not tested here. It is the obvious second fixture and it is the one that would
actually challenge the reranker.

**Stage 1 only.** Q5b — does a *generated answer* rest on the operative document — is not run. A
reranker putting the right document at rank 2 does not establish that an answer would use it over
the withdrawn approval sitting at rank 1 or 3.

**One run, one model pair.** No variance. The reranker is `gpt-5`; a weaker one may well behave as
the prediction said.

## Suggested next fixture

The same shape with the supersession sentence removed: the July decision states its own date and
terms but never mentions March, and March never learns it was replaced. That is the ordinary case in
a real back office, it is what the corpus's own `stale-old` questions look like — where retrieval
scores 0.133 over 15 questions — and it is where a reranker has nothing to read and must fall back on
exactly the topical similarity that put March at 6 and July at 14.
