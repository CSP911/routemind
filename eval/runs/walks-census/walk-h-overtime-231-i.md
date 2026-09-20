1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body

2. **Answer**: Multiplier 2.55x. Minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body

4. **Notes**: The three legends (day, hours, place) had to be resolved separately before the row address could be built — "Liberation Day" → day D3, "eleven hours" → hours H4, "out at a client's office" → place P2, giving row day-d3-hours-h4-place-p2. The near-miss risk was the current-vs-superseded overtime table: /v1/regions/attendance lists both `sec-hard-overtime` (current, in force since 2026-01-01) and older superseded pages (`hard-overtime-v2`, and a `hard-overtime-legend-revision` warning file) with very similar names. Since today is 2026-09-20, the current table was the correct one to use, and its own body confirms the effective-date range. No ambiguity in the legend lookups themselves — all three inputs matched an entry exactly, no nearest-entry guessing was needed.
