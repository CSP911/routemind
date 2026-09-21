# The report

Chapters, written to be read in order by someone who has not seen this repository before. Each one
stands on measurements recorded in `eval/runs/` and names the fingerprint it belongs to.

| | | source |
|---|---|---|
| 1 | Where retrieval breaks | *not yet written* — `eval/COLLAPSE.md`, `eval/runs/2026-09-20-campaign.md` |
| **2** | **[What it costs](02-what-it-costs.md)** | `eval/runs/2026-09-22-cost.md` |
| 3 | A wrong routing table | *not yet written* — `eval/runs/2026-09-21-r6-fix.md` |

**Chapter 2 was written first.** Not the usual order, and there is a reason worth keeping: every
accuracy number this study produced favours routing, and a result reported only on the side it wins
on is an advertisement. The cost column existed as scattered measurements and no chapter. Writing it
first fixes the shape of the argument before the winning numbers get written up around it.

Chapter 1 has to establish, for Chapter 2 to mean anything:

- the corpus and the fingerprint, and that questions and arms share both
- `rag` 0.516 / `rag+rerank` 0.541 / `routing` 0.999 / `routing+overlay` 0.999 over 700 questions
- the lever breakdown, and `indirect` at 0.028 against 1.000 in particular
- that the retrieval arms are a census and the routing arms are now a census too

Chapter 3 has to establish:

- the single miss in 700, and that both routing arms committed it identically
- that the cause was one false sentence in a forwarding note, not a failure of the reader
- `mapcheck` as a precondition, and R6 as the rule written after that failure
- the ten re-walked questions: 0.900 → 1.000 on a new fingerprint, and why those two corpora do not
  merge
