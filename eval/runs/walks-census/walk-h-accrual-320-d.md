1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body

2. **Answer**
For type E4, tenure T3, site L1 (current table, in force from 2026-01-01): accrues 1.52 days per month, with a carry-over limit of 10 days. Today's date (2026-09-20) falls under this current table, so this is what you can still be holding in January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed which version applies for today's date)
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body (the figures)

4. **Notes**
The attendance area lists three versions of the leave accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the revision-legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Since today is 2026-09-20, the current table (`sec-hard-accrual`) is correct, but this was the one place a wrong turn was easy — grabbing a row from `hard-accrual-v2` without checking the date first would have given a superseded number. The current table's row index already keys directly on type/tenure/site (e.g. `hard-accrual-row-type-e4-tenure-t3-site-l1`), so no legend lookup was needed to translate "E4/T3/L1" — the qualifiers in the question matched the address format exactly.
