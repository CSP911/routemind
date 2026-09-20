1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body

2. **Answer**: Multiplier 1.35x; minutes rounded to the nearest 10 minutes. (Ordinary Tuesday = day D1, three hours = hours H2, out at a client's office = place P2.)

3. **Source**:
/v1/nodes/hard-overtime-legend-day (day mapping)
/v1/nodes/hard-overtime-legend-hours (hours mapping)
/v1/nodes/hard-overtime-legend-place (place mapping)
/v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2 (the multiplier and rounding rule)

4. **Notes**: The first instinct was to look under payroll for "overtime," but that area's overtime page is explicitly marked as superseded — a hard warning says overtime premiums moved to attendance on 2026-01-01, and today (2026-09-20) is well past that date, so payroll would have given a stale answer. Inside attendance, there are two overtime tables (a superseded `hard-overtime-v2` and the current `sec-hard-overtime`); picking the current one mattered since the multiplier likely differs by version. The three legends (day/hours/place) are a bit of a trap: "an ordinary Tuesday" maps cleanly to D1, but the day legend's own list mixes actual day-types (Tuesday, Saturday, holiday) with a time-of-day ("two in the morning" → D4), so it's not a pure day-type axis — worth noting in case that oddity is deliberate. No ambiguity in the final row lookup itself once all three codes (D1, H2, P2) were resolved.
