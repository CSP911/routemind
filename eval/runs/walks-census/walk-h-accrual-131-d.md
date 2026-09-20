1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body
./bench/rmcli.py read /v1/nodes/sec-hard-accrual/body

2. **Answer**: For type E2, tenure T4, site L2 (current table, in force from 2026-01-01): accrues 0.98 days per month; carry-over limit (the maximum balance you can be holding into the new year, i.e. in January) is 14 days.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three versions applies to today's date)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body (the figures: 0.98 accrual, 14 carry-over limit)
- /v1/nodes/sec-hard-accrual/body (confirmed "carry-over limit" is the field that answers "how much can I still be holding")

4. **Notes**: The leave-accrual subject has three superseded/current versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns that reaching for the newest is wrong for dates before 2026-01-01 and that the oldest page doesn't announce its own supersession. Today (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-accrual` is correct — but this was worth checking explicitly rather than assuming "current" just because it's the most recently indexed. The row for E2/T4/L2 exists directly under the current table (no need to consult the type/tenure/site legends since the question already gave codes, not descriptions). The only interpretive step was mapping "how much can I still be holding in January" onto the row's "carry-over limit" field — the row itself doesn't use the word "January," so this relies on the sec-hard-accrual overview page's framing of that field as the year-end carry-over cap.
