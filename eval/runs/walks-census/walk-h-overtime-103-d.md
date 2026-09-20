1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body

2. **Answer**: Multiplier is 1.77x; minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body

4. **Notes**: The top-level table list doesn't mention overtime at all, so the first instinct was to check payroll (payslip lines, allowances). Payroll's table explicitly warned that overtime/night/holiday premium rates moved to attendance on 2026-01-01, which redirected the search correctly — without reading that warning it would have been easy to dig through payroll's insurance/payslip sub-tables for nothing. Once in attendance, `sec-hard-overtime` was clearly labeled as the current table (in force from 2026-01-01), separate from two superseded versions (`hard-overtime-v2` and an older `overtime-rate-table`) — the legend-revision warning file made clear those older ones should not be used for a current question. The row address for D2/H1/P4 was printed exactly, so no address construction was needed.
