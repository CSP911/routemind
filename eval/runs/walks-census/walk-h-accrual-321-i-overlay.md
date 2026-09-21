1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 5 years tenure, Busan branch: monthly leave accrual rate and January carry-over cap" --member /v1/regions/attendance "leave accrual rate and carryover/holding limits are attendance domain topics"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c1c0db --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body

2. **Answer**
Accrues 1.54 days per month. Can hold (carry over) at most 11 days into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body

4. **Notes**
The one real fork here was the date/version check: leave accrual has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each with a different indexing scheme, and the legend-revision page explicitly warns not to reach for the newest by reflex. Today's date (2026-09-21) and the fact the question asks about "January" both fall inside the current table's force window (2026-01-01 onward), so `sec-hard-accrual` was the right pick — but it was worth confirming rather than assuming, since the pattern in this doc set is clearly built to punish exactly that assumption.

The three qualifiers mapped cleanly and unambiguously via their legends: "here from our partner firm" → type E4, "been here five years" → tenure T3, "at the Busan branch" → site L2. All three phrases in the question were verbatim matches to legend rows, so there was no nearest-neighbor guessing needed — a rare case where every qualifier lined up exactly.

One cosmetic oddity: `overlay close` reported the five addresses I passed to `--used` as "reached ... from somewhere the overlay never named" because I never ran individual `overlay add` calls for them before closing — I'd only added the top-level `/v1/regions/attendance` member. Didn't affect the outcome, but if overlay bookkeeping matters for future walks, addresses used at close time should probably be added to the working set first.
