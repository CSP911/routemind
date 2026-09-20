1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body

2. **Answer**
0.50 days per month accrue for type E2, tenure/service band T2, under the version in force 2024-07-01 to 2025-12-31 (which covers August 2025).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (identifies which version applies to a 2025 date)
/v1/nodes/hard-accrual-v2/body (the E2/T2 = 0.50 figure)

4. **Notes**
Leave accrual has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and current from 2026-01-01), and the legend page explicitly warns that reaching for the newest table is wrong for any date before 2026-01-01, and that the oldest version doesn't announce that it was ever superseded. Without checking the legend first, it would have been easy to grab the current table (`sec-hard-accrual`) since it's listed as "THE CURRENT LEAVE ACCRUAL TABLE" and reads authoritative — but August 2025 falls in the middle version's window, not the current one. The middle version's table is indexed by two qualifiers (type × tenure) only; site/band as a third qualifier wasn't added until the 2026-01-01 table, so there was no ambiguity about which column to read once the right document was open.
