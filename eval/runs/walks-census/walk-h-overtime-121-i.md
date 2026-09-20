1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body

2. **Answer**: Multiplier 1.95x; minutes are rounded to the nearest 15 minutes. (Also requires advance approval and counts toward the monthly cap.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
- /v1/nodes/hard-overtime-legend-hours/body (six hours → hours H3)
- /v1/nodes/hard-overtime-legend-place/body (out at a client's office → place P2)
- /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body (the multiplier and rounding rule)

4. **Notes**: The attendance table lists three versions of the overtime rate table (`overtime-rate-table`, `hard-overtime-v2`, and `sec-hard-overtime`), each superseding the last, with a legend-revision page explaining which dates each covers. Since today is 2026-09-20 and `sec-hard-overtime` is stated to be in force from 2026-01-01 with no end date, it's the current one — easy to grab a stale row from `hard-overtime-v2` by mistake if you don't check the effective dates first. The day legend was also a minor trap: it mixes a genuine day-type ("a Saturday") with a time-of-day condition ("two in the morning" → D4), so it's not purely a weekday/weekend table — worth reading fully rather than assuming "Saturday" is the only weekend-like row. Otherwise the three legends (day/hours/place) mapped cleanly onto the question's "Saturday / six hours / client's office" with no fuzzy nearest-match judgment needed.
