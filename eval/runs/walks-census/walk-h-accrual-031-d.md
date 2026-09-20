1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body

2. **Answer**: For type E1, tenure T4, site L2 (current table, in force from 2026-01-01, which applies to today's date 2026-09-20): accrues 0.66 days per month. Carry-over limit is 14 days — that is the most you can still be holding into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date)
/v1/nodes/sec-hard-accrual (table listing, confirmed exact row for E1/T4/L2 exists)
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body (source of both figures)

4. **Notes**: The attendance area warns up front that leave accrual has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and that reaching for the newest is wrong for dates before 2026-01-01. Since today is 2026-09-20, the current table (`sec-hard-accrual`) is correct, but it was worth stopping to check the legend rather than assuming "current" was safe by default. The exact row for E1/T4/L2 existed directly in the table listing, so no interpolation across legends (type/tenure/site) was needed. One point of interpretation: the question's "how much can I still be holding in January" isn't phrased as "carry-over limit," but that's the only figure in the row matching a cap on balance held across the year boundary, so I read it as that field.
