1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l3/body

2. **Answer**: For type E1, tenure T1, site L3 (current table, in force since 2026-01-01): accrues 0.44 days per month; carry-over limit is 6 days, i.e. up to 6 days can still be held into January.

3. **Source**:
/v1/regions/attendance
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l3/body

4. **Notes**: The legend-revision page (`hard-accrual-legend-revision`) warns that leave accrual has three versions with different date ranges, and that the oldest one doesn't say it's been superseded — so it would be easy to grab the wrong version if the question's date weren't checked. Today (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so no correction was needed here, but this is exactly the trap the legend warns about for a 2025-dated question. The row itself directly names both requested figures ("Accrues per month" and "Carry-over limit"), so I read "how much can I still be holding in January" as the carry-over limit rather than searching for a separate January-specific rule — there was no other candidate figure on the row or in the table listing that fit better.
