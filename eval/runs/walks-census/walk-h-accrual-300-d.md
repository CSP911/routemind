1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body

2. **Answer**:
For type E4, tenure T1, site L1 (current table, in force since 2026-01-01):
- Accrues 1.36 days of leave per month.
- Carry-over limit is 4 days — that is the most you can still be holding into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body

4. **Notes**:
The attendance area warns up front that leave accrual has three superseded versions (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual`), each covering a different date range, and that the oldest version never says it was replaced — so grabbing the first hit by name would silently give a stale answer. Today's date (2026-09-20) falls under the current table (2026-01-01 onward), so `sec-hard-accrual` was the correct one; a question dated in 2025 would have needed `hard-accrual-v2` instead. Because the question already gave all three qualifiers (type E4, tenure T1, site L1) as codes rather than descriptions, there was no need to open the legend files (site/tenure/type) to translate plain-language terms into codes — the row address could be matched directly from the table listing. The "how much can I still be holding in January" phrasing maps to the row's "Carry-over limit, days" field, not a separate document — worth flagging since it's easy to assume that's a distinct policy elsewhere (e.g. under annual-leave or HR desk) when it's actually part of the same accrual row.
