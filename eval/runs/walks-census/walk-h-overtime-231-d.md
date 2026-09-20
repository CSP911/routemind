1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body

2. **Answer**: Multiplier is 2.55x; minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body

4. **Notes**: The obvious first stop is payroll (payslip lines, overtime rates historically lived there), but its table page explicitly warns that overtime/night/holiday premium rates moved to attendance on 2026-01-01, and the payroll entry is now the superseded page. Following that pointer to /v1/regions/attendance led straight to /v1/nodes/sec-hard-overtime, marked as "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01" — the right one given today's date (2026-09-20). That table also warned of two older superseded versions (hard-overtime-v2 and overtime-rate-table) via hard-overtime-legend-revision; I did not need to open those since the current table directly covers today's date and the D3/H4/P2 row was listed by exact address, so no guessing was needed. The only near-misstep would have been reading the payroll page as authoritative and stopping there.
