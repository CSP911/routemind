# The report

Chapters, written to be read in order by someone who has not seen this repository before. Each rests
on measurements recorded in `eval/runs/` and names the fingerprint it belongs to.

The registered question is `eval/PREREGISTRATION.md` §1: **how useful is human intervention in RAG,
and where does it stop paying for itself?** The intervention is a human-authored routing table. The
chapters take that question in three parts — when the intervention *fails*, what it *costs* when it
works, and what it *buys*.

| | | source |
|---|---|---|
| **1** | **[The moment human intervention fails](01-when-the-intervention-fails.md)** | `eval/runs/2026-09-21-r6-fix.md`, `eval/COLLAPSE.md` |
| **2** | **[What it costs](02-what-it-costs.md)** | `eval/runs/2026-09-22-cost.md` |
| 3 | What it buys, and for which questions | *not yet written* — `eval/runs/2026-09-20-campaign.md` |

## Typeset

`report-en.html` and `report-ko.html` are chapters 1 and 2 together as a single page, with the
figures drawn — hit rate by lever, the collapse curve against its two-parameter fit, cost per
question, and what share of the tree a walk can see. Same content in both, typeset for the language.
Open either in a browser; they need no server and no build.

The markdown chapters remain the source. If a number changes, it changes there first.

## The order these were written in, and why it is not the reading order

**Chapter 2 was written first, then Chapter 1. Chapter 3 — the one with the winning numbers — last.**

Every accuracy figure this study produced favours routing, several by more than an order of
magnitude. A result reported only on the side it wins on is an advertisement. So the cost column was
written up before the accuracy column, and the failure modes before either, to fix the shape of the
argument before the good news got written around it.

Chapter 1 carries the two ways the intervention fails:

1. the table is **wrong**, or stale without anyone meaning it to — measured, one defect, one miss in
   700, both routing arms identically
2. the table is entirely **correct** and at some point fails anyway — **not measured.** One corpus
   size, and a scaling limit cannot be seen from one point

Chapter 3 has to establish, and must not quietly restate Chapter 1's caveats as solved:

- `rag` 0.516 · `rag+rerank` 0.541 · `routing` 0.999 · `routing+overlay` 0.999, over 700 questions
- the lever breakdown, and `indirect` at 0.028 against 1.000 in particular
- that all four arms are now a census, not a sample
- that 320 of the 700 are questions retrieval already answers first time, and this study does not
  argue for walking those
- that `routing+overlay` matches `routing` exactly and costs ×1.16 — a negative result, kept
