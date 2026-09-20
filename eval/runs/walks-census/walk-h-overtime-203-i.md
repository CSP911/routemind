1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body

2. **Answer**: Multiplier 2.25x, minutes rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body

4. **Notes**: The three qualifiers (day type, hours band, place) had to be translated separately through three legend documents before the row address could be assembled — "Liberation Day" → D3, "about ninety minutes" → H1 (the legend uses that exact phrase, so no rounding/nearest-match judgment was needed), and "from home" → P4 (distinct from "on standby at home" = P3, which is a trap for this kind of question — easy to conflate the two "home" entries). The current table (sec-hard-overtime, in force since 2026-01-01) was used rather than the superseded hard-overtime-v2, consistent with today's date of 2026-09-20.
