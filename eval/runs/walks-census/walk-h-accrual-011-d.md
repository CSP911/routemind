1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body
./bench/rmcli.py read /v1/nodes/sec-hard-accrual/body

2. **Answer**: For type E1, tenure T2, site L2 (current table, in force since 2026-01-01): accrues 0.50 days per month; carry-over limit (the most that can be held/carried into January) is 8 days. Notice required to use leave is 3 working days; leave does not accrue during unpaid leave.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirmed current table applies for 2026-09-20)
/v1/nodes/sec-hard-accrual/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body

4. **Notes**: The main risk here was picking the wrong version of the accrual table — this subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Since today's date (2026-09-20) falls after 2026-01-01, the current table (`sec-hard-accrual`) is correct, but I checked the revision page first rather than assuming. The question's "how much can I still be holding in January" phrasing doesn't literally say "carry-over limit," but it maps directly onto that field in the row document — the carry-over limit is exactly the cap on balance held across the year boundary into January, so no further table (e.g., a separate January-specific cap) exists or was needed.
