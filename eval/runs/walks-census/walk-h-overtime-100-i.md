1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body

2. **Answer**: Multiplier 1.68x; minutes rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body

4. **Notes**: The overtime table has 64 rows (day D1-D4 × hours H1-H4 × place P1-P4), and none of the row labels use plain-language terms — you must resolve each qualifier through its own legend first (Saturday → D2, "about ninety minutes" → H1, "at my desk" → P1) before the row address can even be constructed, and the table explicitly warns never to build an address yourself, only use ones a table printed — so the three legend reads were mandatory, not optional shortcuts. The one place I could have gone wrong: `sec-hard-overtime` is explicitly labeled the current table (in force from 2026-01-01, today's date), with superseded versions (`hard-overtime-v2`, `overtime-rate-table`) sitting right next to it in the attendance area listing — easy to grab the wrong one if not reading the "WARNING" and "SUPERSEDED" labels carefully. "About ninety minutes" mapping straight to H1 with no closer numeric band was also worth double-checking against the legend's fallback rule ("nearest entry above it"), but it turned out to be an exact listed match, not a nearest-fit judgment call.
