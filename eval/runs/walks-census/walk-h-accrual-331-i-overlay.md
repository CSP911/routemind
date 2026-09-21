1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 9 years tenure, Busan branch: monthly leave accrual rate and max carryover holdable in January" --member /v1/regions/attendance "leave accrual and carryover rules live here"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_eb90a7 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body

2. **Answer**
Accrues 1.62 days per month. Carry-over limit is 14 days (this is the maximum that can still be held into January).

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body

4. **Notes**
The legends are the whole trick here: "here from our partner firm" only maps to a type code (E4) via the exact phrase in hard-accrual-legend-type — general knowledge of "partner firm" as a contractor category would not have produced the right row. Likewise "been here nine years" maps to T4 and "at the Busan branch" maps to L2 only through the tenure and site legends, which use the caller's own wording as the left-hand column. Skipping any one of the three legends risks guessing the wrong row out of 64.

There are three versions of the accrual table (hard-accrual-legend-revision flags this explicitly): a superseded v2 (2024-07-01 to 2025-12-31), an older `leave-accrual`, and the current `sec-hard-accrual` in force from 2026-01-01. Today's date (2026-09-21) falls inside the current version's range, and since it has no stated end date, it also covers the January the caller is asking about — so no version-switching was needed, but it would have been easy to grab the wrong era's row without checking hard-accrual-legend-revision first.

Minor oddity: `overlay close` reported all four addresses I used as "reached... from somewhere the overlay never named" rather than as overlay members — I only ever added /v1/regions/attendance as a member and then read further rows directly via `table`/`read` rather than adding each one with `overlay add`. Answer is unaffected, but the overlay's own record of "what was in the working set" undercounts what was actually consulted.
