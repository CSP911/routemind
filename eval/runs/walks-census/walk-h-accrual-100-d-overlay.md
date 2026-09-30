1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T1, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carry/cap rules for leave are in attendance area"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9504d3 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body

2. **Answer**:
For type E2, tenure T1, site L1: accrues 0.72 days per month, with a carry-over limit of 4 days. Since today (2026-09-21) and the "January" in the question both fall under the table in force from 2026-01-01, the current table applies: the most you can still be holding (carried over) is 4 days.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual table versions applies to a 2026 date)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body (the E2/T1/L1 row: 0.72 days/month accrual, 4-day carry-over limit)

4. **Notes**:
Leave accrual has three superseded/current versions indexed by date, and the legend-revision page explicitly warns that reaching for the newest version is wrong for any date before 2026-01-01 — the oldest version also doesn't flag itself as superseded, which is the trap. Today's date (2026-09-21) and the January the question refers to both sit inside the current table's effective range (2026-01-01 onward), so there was no version ambiguity here, but I read the revision-legend page first specifically to rule that out before trusting `sec-hard-accrual`. The "how much can I still be holding in January" phrasing is a plain-language stand-in for "carry-over limit," which the row states directly (4 days) rather than requiring any computation from the monthly rate.
