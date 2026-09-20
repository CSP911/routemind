# supplier-selection-silent — Q5a, run before proposing it

    2026-09-21 · baseline: ontology/service/ unchanged since baseline-pre-continuity
    783 documents in the pool (779 corpus + 4 fixture) · k=10 · fused n=20
    embed text-embedding-3-large · rerank gpt-5

Run before the pull request was opened, not after, so the proposal arrives with its own result
attached rather than as a guess about what it would show.

| arm | found | operative | n |
|---|---|---|---|
| `rag` | **1.000** | **0.333** | 3 |
| `rag+rerank` | **1.000** | **0.333** | 3 |

## This is the distinction, as cleanly as it can be shown

**`found` is perfect. `operative` is one in three.** Every document is retrievable; the system simply
prefers the wrong one. There is no retrieval failure anywhere in this table — and the answers built
from the top of these lists would be wrong twice out of three times.

| question | operative rank | outranked by |
|---|---|---|
| Which supplier is currently approved for Y? | 2 | `y-supplier-c-approved` at **1** |
| Can I place a new order for Y with Supplier C? | 2 | `y-supplier-c-approved` at **1** |
| What delivery window applies to a Y order placed today? | 1 | — |

The February registration outranks the September one for *"which supplier is currently approved"*.
Both are real registrations, both went through the desk against three quotes, and only the dates
separate them.

## The reranker gains nothing here

On `supplier-selection-x` the reranker took `operative` from 0.667 to 1.000. Here it moves one rank
(question 2, from 6 to 2) and changes no verdict: **0.333 either way.**

The difference between the two fixtures is one sentence. GovKM's original says *"This replaces the
approval of Supplier A dated 3 March 2025"*; nothing in this one says anything of the kind. So the
prediction in `eval/PREREGISTRATION.md` §Q5a — *"a reranker blind to dates has no reason to put July
above March"* — is right after all, and the first fixture had not disproved it so much as handed the
reranker a sentence to read.

That is the useful shape of the result: **the reranker is not reasoning about currency, it is reading
whoever wrote it down.** When nobody wrote it down, it ranks on topical similarity and the superseded
decision wins, because a February registration and a September registration are near-identical
documents and the question's words do not favour either.

## What it does not establish

**n=3, one fixture, one run.** 0.333 is "one of three". Nothing here carries an interval.

**Written to make a prediction fail.** Declared in the fixture's own header and repeated here,
because a test built to produce a wanted result is worth suspecting. The guards are that
`supplier-selection-x` stays beside it untouched as the control, and that the difference between them
is a single removed sentence rather than a redesign. Whether the scenario is *realistic* is the part
a contributor should judge, not the author.

**Stage 1 only.** Q5b — whether a generated answer rests on the operative document — is not run, and
is where this fixture would say the most: with the wrong document at rank 1 and the right one at 2,
what an answer actually uses is an open question, not a foregone one.

**The corpus agrees, at larger n.** `stale-old` in the main study — a question about a version two
revisions back, where no document announces its own supersession — scores 0.133 for `rag` and 0.200
for `rag+rerank` over 15 questions. This fixture is the same failure isolated to four documents.
