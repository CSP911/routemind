# `supplier-selection-retrospective` — the one run

Run once, 2026-10-01 23:15, after GovKM froze the fixture, the map, the review page and the
predictions on PR #1 (2026-09-30 13:59 and 2026-10-01 01:12). Nothing in those four files was
touched after the output was seen; the predictions in `supplier-selection-retrospective.review.md`
§6 stand exactly as written, including the one that was wrong.

| record | what |
|---|---|
| `eval/runs/2026-10-01-q5a-retrospective.json` | every arm's ranks, and for routing every walk: each turn as the model wrote it, what it opened, what it read, in what order, and what it cost |
| `eval/runs/2026-10-01-q5a-retrospective.log` | the console of that run, verbatim |
| commit `corpus-2026-09-20-55-g249dec7` | the pool: 784 documents, 5 from this fixture, `k=10` |

**n=4, one run each.** `0.250` is "one question of four". No interval attaches to any figure here.

---

## Predicted and observed

| arm | predicted found | observed | predicted operative | observed |
|---|---|---|---|---|
| `rag` | 1.000 | **1.000** | 0.250 | **0.250** |
| `rag+rerank` | 1.000 | **1.000** | 0.250 | **0.250** |
| `routing` | 1.000 | **0.750** | 1.000 | **0.500** |

Two predictions held to the digit. The third did not, and it is the one about the arm this
repository exists to argue for.

## Per question

`rank` is the position of the operative document — for the retrieval arms in the fused or reranked
list, for routing in the order the walk *read* documents. `operative` is that rank being above every
distractor's. The same `score_question` scores all three arms; the definition is in `score.py`.

| | question | operative | rag | rag+rerank | routing |
|---|---|---|---|---|---|
| 1 | Which supplier is currently approved for Z? | `z-supplier-f-approved` | rank 2 — behind **Feb** | rank 2 — behind **Feb** | **rank 1 ✓** |
| 2 | Can I place a new order for Z with Supplier E? | `z-supplier-f-approved` | rank 8 — behind **Feb** | rank 2 — behind **Feb** | rank 8 — behind **Feb** at 7 |
| 3 | What delivery window applies to a Z order today? | `z-supplier-f-approved` | rank 2 — behind **Feb** | rank 2 — behind **Feb** | **not read** — walk exhausted |
| 4 | How did Supplier E perform while it held Z? | `z-supplier-e-performance-review` | **rank 1 ✓** | **rank 1 ✓** | **rank 2 ✓** (no distractor read before it) |

"Feb" is `z-supplier-e-approved`, the superseded February registration.

### What the retrieval arms did

On every current-state question both arms put the **February registration first** and the September
one second. The reranker changed one rank (Q2, 8 → 2) and no verdict — the same thing it did on the
silent fixture. The December review, the document this variant was built around, **did not outrank
the operative decision in either retrieval arm on any question.** The relevance trap fired; the
recency trap did not. On Q4 both arms found the review at rank 1.

### What the walk did, question by question

From the walk logs in the run record. The map's node is `sec-z-component-sourcing`, under
`procurement › vendor › sec-vendor-registration-cases`.

**Q1 — 4 hops, 10 turns.** `procurement › vendor › sec-vendor-registration-cases ›
sec-z-component-sourcing`, then READ `z-supplier-f-approved` and nothing else. The map was read and
followed.

**Q2 — 9 hops, 19 turns, one return to hop 0.** Opened `sec-vendor-performance-and-renewal`, read
`renewal-decision` and `ending-a-vendor-relationship`; went back; opened `sec-supplier-due-diligence`,
read two more; `purchase-request`, read one; `vendor`, read `vendor-steps`; then
`sec-vendor-registration-cases › sec-z-component-sourcing`. At the map it read **`z-supplier-e-approved`
first** — the row the question names, whose map line says *replaced on 1 September 2025 and not the
source for a new order* — then `z-supplier-f-approved`, then the November note. By the frozen
definition that is the operative document read eighth and a distractor read seventh: an ORDER
failure. The transcript shows the walk reading the named row, seeing it marked replaced, and opening
the one marked current; the metric does not distinguish that from preferring the wrong document, and
it was not designed to.

**Q3 — 23 hops, 30 turns, six returns to hop 0, exhausted.** `purchase-request › purchase-steps`;
back; `sec-receiving-and-inspection › receiving-overview`; back; `ga-desk › ga-contact`; back;
`procurement-overview`; `sec-contract-terms-the-company-insists-on › standard-payment-terms`; back;
`approval-threshold › threshold-table`; back; `vendor › vendor-form › vendor-form-fields`; back;
`sec-vendor-performance-and-renewal` — and the turn ceiling. **The walk never opened
`sec-vendor-registration-cases` and never saw the map.** It read seven documents, none from the
fixture.

**Q4 — 11 hops, 17 turns, two returns.** `sec-vendor-performance-and-renewal › missed-delivery-dates`
(read); back; `sec-receiving-and-inspection`, `sec-supplier-due-diligence`; back; `vendor ›
sec-vendor-registration-cases › sec-z-component-sourcing`, READ `z-supplier-e-performance-review`.
Found, and no distractor read before it. The history row advertised as history was reachable when
history was asked for — the half of the requirement question 4 exists to check.

## The observation the logs force

The map was obeyed every time it was reached. Q1 and Q4 reached it and were answered from it; Q2
reached it after seven detours and was answered from it, in an order the metric counts against it;
Q3 never reached it. So the routing arm's 0.500 is not, on this evidence, a failure of the map's
`current / replaced / history` declarations. It is a failure to **arrive at the map** — and the
reason is readable in the lines above it, checked after the run with a literal word match against
the four questions:

| line on the way down | words of any question it contains |
|---|---|
| `procurement` — hop 0, frozen use_when | *approved* |
| `vendor` — "How a new supplier is registered and which papers they have to give you" | *supplier* |
| `sec-vendor-registration-cases` — "Addressing special vendor registration scenarios and challenges" | **none** |
| `sec-z-component-sourcing` — the map's node, three levels down | *component* |

"Z", "delivery", "window" appear in no line between hop 0 and the map. The map's one sentence sits
beneath a signpost that says nothing a Z question says, under an area whose frozen sentence says
nothing about components or delivery windows. A walk that reads lines had nothing to follow on Q3
and little on Q2, and went where the words did lead — payment terms, receiving, renewal.

This is a finding about the arrangement, stated as the frozen design stated it: the map was
reviewed as *the system under test*, and the review page's §7.1 asked whether the map is a fair
place to put the continuity statement. The run answers a narrower question first — the statement
is only read if the walk gets there, and nothing above it was written to bring a walk there. The
fixture froze the map's lines and did not freeze the ancestors' lines, so nothing here was
tuned to fix that, and nothing will be on this branch.

## Interpretation boundary, as agreed

GovKM, 2026-10-01: *a routing success demonstrates that curated continuity metadata can preserve and
expose authority/history distinctions. It should not be described as the system independently
inferring authority or supersession from the document corpus.* The two routing successes here are
exactly that — a person wrote `current` on one row and `history` on another, and a walk that read
those rows obeyed them. The two routing failures are a walk that did not read those rows. Neither
is an inference by the system about authority, and this page does not call them one.

## Things that are not results

- `baseline: NO`. `score.py` diffs `ontology/service/` against `baseline-pre-continuity` and reports
  that it has changed (ages, peers, sessions, validation — 8 files since 2026-09-18). The retrieval
  harness in `bench/` does not import that service, and the retrieval figures on this page were
  produced by the same code that produced the silent fixture's; the line is printed because the
  scorer promised to print it the day it stopped being true, and this is that day.
- The walker is `bench/agent.py` (`claude-opus-5`, 30-turn ceiling, frozen hop-0 sentences) — the
  pilot's in-process walker, chosen because it writes every turn into the run record. It is not the
  `claude -p` walker the 700-question census used, and no figure here should be read against those.
- One run. Q3's exhaustion and Q2's detours are one walk each at one temperature; a second run was
  not made and will not be made against this expectation.
