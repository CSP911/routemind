1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T3, site L3: monthly leave accrual rate and January carryover cap" --member /v1/regions/attendance "leave accrual rate and carryover/cap rules likely live in attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_86b274 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body

2. **Answer**:
Accrual: 0.92 days per month.
Carry-over limit (max you can still be holding into January): 12 days.
(This row also notes: 5 working days' notice required to take leave, and no accrual during unpaid leave.)

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual table versions applies to today's date, 2026-09-20/21 — the current one, in force from 2026-01-01)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body (the actual figures: 0.92 days/month accrual, 12-day carry-over limit)

4. **Notes**:
The attendance area's overlay listed three separate leave-accrual documents at different addresses (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with an explicit warning that reaching for the newest one is wrong for dates before 2026-01-01. Since today (2026-09-20) falls after that cutover, `sec-hard-accrual` (the current table) was correct, but this was a real fork in the walk — a question dated in 2025 would have needed `hard-accrual-v2` instead, and naively grabbing "the current table" without checking the revision-legend first would have been a plausible mistake.

The overlay-close output flagged both addresses I listed as "reached ... from somewhere the overlay never named" rather than as members I'd explicitly added — I read them directly from the table listing without an explicit `overlay add`, which the tool still tracked but noted separately. Worth being more disciplined about adding members before reading in future walks, even when a table listing is the obvious next hop.

No ambiguity in mapping E2/T3/L3 to the row: the question's own vocabulary (type/tenure/site codes) matched the table's indexing exactly, so the legend files for site/tenure/type codes weren't needed to disambiguate.
