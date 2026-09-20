1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body
./bench/rmcli.py read /v1/nodes/sec-hard-accrual/body

2. **Answer**: For type E3, tenure T3, site L4 (current table, in force since 2026-01-01): accrues 1.26 days per month; carry-over limit is 13 days — that is the most you can be holding over into the new year (January).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies for today's date, 2026-09-20)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body (the figures: 1.26 days/month accrual, 13-day carry-over limit)
- /v1/nodes/sec-hard-accrual/body (confirms "carry-over limit" is the general cap stated per row, not a separate January-specific figure)

4. **Notes**: The area listing flags up front that leave accrual has three versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with the oldest giving no indication it was ever superseded — an easy trap if you grab the first hit instead of checking dates. Today (2026-09-20) falls under the current table, so that trap didn't bite here, but it would have for any question dated before 2026-01-01. The "January" phrasing in the question suggested there might be a distinct year-end/January-specific carryover rule, but the source only defines a single "carry-over limit" per row with no January-specific variant — I read the table-level body to confirm there wasn't a second, separate figure I was missing before settling on that interpretation.
