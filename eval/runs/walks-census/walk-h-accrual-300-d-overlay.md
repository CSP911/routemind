1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T1, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rates and carryover/cap rules by employee type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d19539 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body

2. **Answer**
For type E4, tenure T1, site L1 (current table, in force 2026-01-01 onwards):
- Accrues 1.36 days per month.
- Carry-over limit is 4 days — that is the most you can still be holding in January (i.e. the cap on what carries into the new year).

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date)
- /v1/nodes/sec-hard-accrual (current accrual table, located the E4/T1/L1 row)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body (the figures: 1.36 days/month accrual, 4-day carry-over limit)

4. **Notes**
- This topic has three superseding versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no indication on the oldest that it was ever replaced — the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20/21) falls inside the current table's range, so `sec-hard-accrual` was correct, but this is exactly the kind of question where grabbing the first accrual-looking hit without checking the date would silently give the wrong version for a mid-2025 question.
- "How much can I still be holding in January" is worded ambiguously — it isn't asking for a leave balance lookup, it's asking about the carry-over cap (the limit on unused days that survive into the new year). The row's "Carry-over limit" field answers it directly; I didn't need the annual-leave or attendance-system tables for this.
- I read the two supporting documents (legend-revision, sec-hard-accrual table) directly via `table`/`read` without first adding them as overlay members — the close command flagged them as "reached" (answered from somewhere the overlay never named) rather than a clean hit against a pre-declared member. Functionally fine here since the question mapped straight to one row, but for a less direct question I'd want to `overlay add` each address as I open it, per the intended narrowing workflow.
