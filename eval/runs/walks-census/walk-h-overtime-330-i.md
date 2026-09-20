1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body

2. **Answer**: Multiplier 3.00x. Minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime (table)
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body

4. **Notes**: The three qualifiers in the question map to legend entries almost too literally — "two in the morning" is listed verbatim as day D4, "eleven hours" verbatim as hours H4, and "at my desk" verbatim as place P1, so no interpolation via the "nearest entry above it" fallback was needed. The one place this could have gone wrong: the attendance area lists both a current overtime table (`sec-hard-overtime`, in force since 2026-01-01) and superseded ones (`hard-overtime-v2`, `overtime-rate-table`) — picking the wrong vintage would have silently given an old multiplier/rounding pair. Today's date (2026-09-20) falls inside the current table's validity, so `sec-hard-overtime` was the correct pick, confirmed via the "in force from 2026-01-01" note on the row itself.
