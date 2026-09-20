1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body

2. **Answer**: Multiplier 1.86x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body

4. **Notes**: The walk was straightforward — the attendance region's description explicitly mentions "what overtime, night and holiday hours pay, by day type, hours and place (current table since 2026-01-01)," which pointed directly at `sec-hard-overtime`. That table's listing also names a superseded `hard-overtime-v2` and an older `overtime-rate-table`, plus a `hard-overtime-legend-revision` warning about three versions with different rates — worth flagging because it would be easy to grab a row from the wrong (superseded) version if not careful. I confirmed `sec-hard-overtime` is the current table (in force from 2026-01-01, which matches today's date of 2026-09-20) before reading the D2/H2/P3 row, and did not need to consult the legends since the question already gave codes (D2, H2, P3) directly rather than plain-language descriptions.
