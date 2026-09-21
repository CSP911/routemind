1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In August 2025, how much leave was accrued or granted for type E2 staff in service band T2? Answer under the version of leave accrual that was in force on that date." --member /v1/regions/attendance "leave accrual info likely lives under attendance region"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_1c424e --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-v2/body

2. **Answer**: 0.50 days accrued per month for type E2, tenure/service band T2, under the version of leave accrual in force 2024-07-01 to 2025-12-31 (which covers August 2025).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (established which of the three accrual versions applies to a August 2025 date)
- /v1/nodes/hard-accrual-v2/body (the actual E2/T2 rate table for the 2024-07-01–2025-12-31 version)

4. **Notes**: The attendance overlay table surfaces three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no obvious hint from titles alone which one is current versus superseded versus forthcoming. The legend-revision doc explicitly warns that reaching for the newest (`sec-hard-accrual`, in force from 2026-01-01) is wrong for a 2025 date, and that the oldest (`leave-accrual`) says nothing about being superseded — so skipping the legend page and reading only the table titled "THE CURRENT LEAVE ACCRUAL TABLE" would have silently produced the wrong-era figure. Checking the legend first before reading any rate table was the right call and avoided that trap.
