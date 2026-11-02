# Where a succession statement is written decides whether a walk reads it — 2026-11-02

Exploratory. One question: the same four facts (Supplier C registered 17 Feb 2025, Supplier D
registered 1 Sep 2025, nothing in the documents says D replaced C), presented five ways. Which
presentation lets a model pick the document that governs? `make.py` generates the five from
`supplier-selection-silent.yaml`, so the difference between any two is exactly what that file says.

| | where the succession is written |
|---|---|
| a silent | nowhere — dates in the prose only; map rows are each document's own line |
| d dates-in-row | map rows add each decision's date; no succession words |
| b doc-header | the two documents open with RFC-style lines, `Supersedes:` / `Superseded by:` |
| c row-statement | the map rows say it in words, with the period each was in force |
| e both | b + c |

Walker: `bench/agent.py` with the model call sent to an isolated `claude -p --model claude-sonnet-5`
(`wrapper.py`; the API credit is exhausted — the same deviation as the 2026-10-10 exploratory run).
30-turn ceiling. Three runs per variant. Retrieval: cached text-embedding-3-large; the gpt-5 reranker
ran once per variant before the OpenAI credit ran out, so its row is n=1 and lacks variant c.

## Routing — reached the node / read the governing document before its distractor, of 3 runs

| question | a | d | b | c | e |
|---|---|---|---|---|---|
| Q1 which supplier is currently approved | 3/3 · 1/3 | 3/3 · 1/3 | 3/3 · 0/3 | 3/3 · **3/3** | 3/3 · **3/3** |
| Q2 can I order from C (names the distractor) | 3/3 · 0/3 | 3/3 · 0/3 | 3/3 · 0/3 | 3/3 · 0/3 | 3/3 · 0/3 |
| Q3 delivery window today | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| Q4 as of April 2025 (C governs) | 2/3 · 2/3 | 2/3 · 2/3 | 1/3 · 1/3 | 1/3 · 1/3 | 0/3 |
| Q5 delivery window as of March 2025 (C governs) | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 |

## Reranker (gpt-5 over 20 fused candidates), one run

| | a | d | b | e |
|---|---|---|---|---|
| operative, of 5 | 3 | 3 | **5** | **5** |

Variant c's documents are byte-identical to a's (the statement is in the map, which retrieval never
sees), so its reranker row would be a's.

## What it says

1. **A statement in the row is read before any document is opened.** On Q1, variants c and e read
   `y-supplier-d-approved` and nothing else, 6 runs of 6. Every other variant read C first and then
   D (7 of 9 runs), the documents in the order of their dates, and the scorer's order rule counts
   that as the wrong document preferred. The header in the document (b) did not change the walk at
   all: the walker opens C before D either way, and reads the header too late.
2. **Dates in the row do nothing.** d is a in every number. The model is not comparing two dates
   in a table; it is reading sentences.
3. **The reranker reads the header.** With `Supersedes:` / `Superseded by:` at the top of the
   documents it went from 3/5 to 5/5 — GovKM's 2026-09 finding, reproduced on generated text. The
   row statement cannot reach it, because retrieval reads documents and not the map.
4. **A question that names the distractor is not rescued by any presentation.** Q2 reads C first in
   all 15 runs. The walker goes to what the question names, then to what the row says governs —
   the "relevance wins" pattern GovKM named on 2026-10-09. In c r3 it read C only: the row had
   already answered the question. Whether that is a failure is a scoring question (what was read
   before what) rather than a routing one; the answer it would give is right.
5. **Reachability dominates the rest.** Q3 and Q5 never reached the fixture's node in any variant
   (15 of 15 walks went to receiving and contract terms), and Q4 reached it in 6 of 15. The node's
   line — "the registrations and records for the Y component's supplier" — does not name delivery
   windows or past orders, so a walk looking for those never descends to it. That is docs/WRITING.md
   rule 1 (a line names every question its pages answer), not a presentation effect, and it is the
   same in all five variants. The as-of questions therefore say nothing yet about whether the
   period words in the row ("from 17 February 2025 — replaced on 1 September 2025") are used.

## What it does not establish

n=3 walks per cell, one model, one fixture family, generated text. The reranker row is n=1. No
variance beyond "3 of 3". Q4/Q5 need a node line that reaches them before the as-of claim can be
tested at all.

## Next

- The reachability fix is a line, not code: give the node a line that names delivery windows and
  past orders, rerun Q3–Q5. That is the F experiment's "map written by a person" step in miniature.
- The row statement is what RouteMind's map is for. The experiment is the reason to write it into
  docs/WRITING.md as a rule: *when one record replaces another, say so in the row — the period each
  was in force, and the address of the one that follows* — and to put the RFC-style line at the top
  of the document as well, for whoever reads documents without the map.
