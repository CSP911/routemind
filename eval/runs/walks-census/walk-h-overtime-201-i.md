1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body

2. **Answer**: Multiplier is 2.19x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
- /v1/nodes/hard-overtime-legend-place/body (out at a client's office → place P2)
- /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body (multiplier and rounding)

4. **Notes**: The payroll table's own overtime page (`sec-hard-overtime`'s payroll-side sibling) is a trap: payroll's index says overtime premiums moved to attendance on 2026-01-01 and the payroll page is "the old rule," so I had to redirect to /v1/regions/attendance instead of reading the payroll overtime file. Within attendance, there were three overtime tables (`hard-overtime-v2`, superseded `overtime-rate-table` referenced in warnings, and the current `sec-hard-overtime`) — the legend-revision warning file made clear `sec-hard-overtime` is the one in force since 2026-01-01, which matches today's date (2026-09-20), so I used that one and never opened the superseded versions. All three qualifiers in the question (Liberation Day, ~90 minutes, client's office) matched their legend rows exactly with no nearest-entry judgment calls needed.
