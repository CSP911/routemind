1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body

2. **Answer**: Multiplier is 1.95x; minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body

4. **Notes**: The trail was easy to lose only because payroll looked like the natural first stop (payslip lines, allowances, etc.) — but payroll's own table page warns that overtime premiums moved to attendance on 2026-01-01, and points there explicitly. Once in attendance, `sec-hard-overtime` was clearly marked as "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," which matches today's date (2026-09-20), so no need to consult the superseded `hard-overtime-v2` or `overtime-rate-table` versions. The table listed all 64 day/hours/place combinations directly by address, so the D2/H3/P2 row could be selected exactly without guessing at an address — no legend lookups were needed since the question already gave codes (D2, H3, P2) rather than plain-language descriptions.
