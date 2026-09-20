1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p2/body

2. **Answer**: Multiplier 1.59x; minutes rounded to the nearest 20 minutes. (Also: approval needed in advance, and counts toward the monthly cap.)

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p2/body

4. **Notes**: The payroll region's overtime page (`/v1/nodes/hard-moved-overtime`) is a trap — it warns that overtime premiums moved to attendance on 2026-01-01, so the real answer lives there instead. Within attendance, there are three overlapping "overtime rate" tables (a superseded `hard-overtime-v2` for 2024-07-01–2025-12-31, an even older `overtime-rate-table`, and the current `sec-hard-overtime` in force from 2026-01-01); since today's date is 2026-09-20, only the current table applies — easy to grab a stale one by accident if you don't check the "in force" dates. The three legends (day/hours/place) had to be read before the row address could be built, since none of D1/H4/P2 are guessable from the question's wording alone. All three inputs in this question happened to match a legend entry exactly ("an ordinary Tuesday" → D1, "eleven hours" → H4, "out at a client's office" → P2), so no nearest-entry judgment call was needed here — but it's the kind of place a walk would silently go wrong if the wording didn't line up exactly.
