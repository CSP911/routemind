1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body

2. **Answer**: For type E3, tenure T3, site L1 (current table, in force from 2026-01-01): accrues 1.20 days per month; carry-over limit is 10 days — that is the most that can still be held into January.

3. **Source**: /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body

4. **Notes**: The attendance area flags that leave accrual has three versions covering different date ranges (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), with an explicit warning that reaching for the newest table is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls in the current version's range, so `sec-hard-accrual` was the correct table — but this was the one place a wrong turn was easy: grabbing `hard-accrual-v2` or the oldest `leave-accrual` node by habit would have given a stale rate/limit. The row for E3/T3/L1 was listed directly in the table by qualifier codes, so no legend lookup was needed to translate the question's own codes. I read "how much can I still be holding in January" as the carry-over limit (10 days), since the row's own field is literally named "Carry-over limit, days" and no separate January-specific figure exists in this row.
