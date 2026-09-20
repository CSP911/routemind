1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body

2. **Answer**: Multiplier 2.37x. Minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body

4. **Notes**: The obvious first stop was payroll (it lists overtime-sounding pages), but its own table header warns that overtime/night/holiday premium rates moved to attendance on 2026-01-01 and that the payroll page is the old rule — payroll would have been a wrong, stale answer if I'd stopped there. Attendance then has two full generations of overtime table (`hard-overtime-v2`, superseded, and `sec-hard-overtime`, current since 2026-01-01) plus a `hard-overtime-legend-revision` warning page about three total versions; I only opened the current one and didn't need to open the superseded ones, but it would be easy to grab the wrong version by address-guessing rather than reading the "current since" wording. The three legends (day/hours/place) had to be resolved separately before the row address could be built, and each legend explicitly says "take the nearest entry above it" if the exact value isn't listed — in this case all three inputs (Liberation Day, three hours, from home) matched an exact row, so no nearest-entry judgment call was needed. No ambiguity in the final row itself.
