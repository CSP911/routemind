1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body

2. **Answer**: Multiplier 3.06x; minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body

4. **Notes**: Straightforward walk — /v1/regions/attendance's description explicitly named "overtime, night and holiday hours pay, by day type, hours and place (current table since 2026-01-01)," which matched the D/H/P shape of the question directly, and /v1/nodes/sec-hard-overtime's listing spelled out the exact row address (day-d4-hours-h4-place-p3) with no ambiguity. The one thing worth flagging: the overtime table's own note says this is the third of three versions (`hard-overtime-v2` for 2024-07-01–2025-12-31, and `overtime-rate-table` before that) — it would be easy to grab a superseded row by address-guessing instead of walking through the current table, but since the walk only ever printed addresses under `sec-hard-overtime` (the current, in-force table) there was no risk of that here.
