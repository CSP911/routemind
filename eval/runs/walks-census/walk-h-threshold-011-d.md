1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body

2. **Answer**: For category C1, amount V2, term M2 (current table, in force from 2026-01-01): the department head signs it off. Yes, other prices are required first — two competing quotes. Delegation limit is 5005 thousand KRW, and 6 working days should be expected.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed the current, 2026-01-01-onward table applies to today's date)
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body (the answer)

4. **Notes**: The procurement area warns up front that the approval-threshold subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and that reaching for the newest one is wrong for any question dated before 2026-01-01. It would have been easy to jump straight to `sec-hard-threshold` since it's the "current" table, but I checked the legend-revision page first to confirm today's date (2026-09-20) actually falls in the current version's range — it does, so no correction was needed here, but a question dated in 2025 would have required the `hard-threshold-v2` page instead. The row for C1/V2/M2 existed directly under `sec-hard-threshold` (no need to interpret separate category/amount/term legends since the question already gave the codes literally), which kept the walk short.
