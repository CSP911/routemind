1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body

2. **Answer**: Multiplier is 1.92x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body

4. **Notes**: The three legends (day, hours, place) had to be resolved separately before the row address could be built — "a Saturday" → D2, "six hours" → H3, "at my desk" → P1, giving row d2-hours-h3-place-p1. It would have been easy to grab the wrong table: there are three superseded versions of the overtime rate (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime`), each with their own legend/warning nodes, so I checked the row's own "in force from 2026-01-01" note against today's date (2026-09-20) to confirm the current table applies rather than assuming from the table description alone. The day legend's fourth entry ("two in the morning" → D4) is a time-of-day value mixed into what looks like a day-type column, which is a trap if you're skimming for "Saturday" without reading all rows carefully — D2 is the correct and unambiguous match here.
