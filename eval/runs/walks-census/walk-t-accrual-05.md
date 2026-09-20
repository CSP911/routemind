1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body

2. **Answer**: 0.50 days accrued per month for type E2, service band T2, under the accrual rule in force 2024-07-01 to 2025-12-31.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (identified which version applies to March 2025)
- /v1/nodes/hard-accrual-v2/body (the table with the E2/T2 figure)

4. **Notes**: There are three versions of the leave accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the attendance table's own listing describes `sec-hard-accrual` as "THE CURRENT LEAVE ACCRUAL TABLE" — it would be easy to grab that one by reflex since it's flagged as current, but it only applies from 2026-01-01 onward. The legend-revision page explicitly warns against reaching for the newest table and states that for a 2025-dated question the middle version (`hard-accrual-v2`, in force 2024-07-01 to 2025-12-31) is the correct one. March 2025 falls squarely in that window, so `hard-accrual-v2` is correct, not the current table.
