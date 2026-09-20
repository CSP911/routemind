1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body

2. **Answer**:
Under the current accrual table (in force since 2026-01-01, which applies since today is 2026-09-20), for type E4, tenure T2, site L4:
- Accrues 1.50 days per month.
- Carry-over limit is 10 days — this is the most you can still be holding into January.
- (Also on file: notice required to take leave is 5 working days, and leave does not accrue during unpaid leave.)

3. **Source**:
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body

4. **Notes**:
There are three versions of the leave accrual table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`), so no adjustment was needed here, but this was the one place the walk could easily have gone wrong if the date check had been skipped. Since the question already gave the type/tenure/site codes (E4/T2/L4) directly, the row was found in a single lookup from the table listing without needing the separate site/tenure/type legend files.
