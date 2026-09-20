1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body

2. **Answer**: Multiplier 1.74x, minutes rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
- /v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
- /v1/nodes/hard-overtime-legend-place/body (on standby at home → place P3)
- /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body (multiplier and rounding)

4. **Notes**: The three legend tables map the question's phrasing to codes almost verbatim — "a Saturday" for D2, "about ninety minutes" for H1, and "on standby at home" for P3 are the exact example phrasings, not approximations, so there was no ambiguity in picking the row. The one place I paused was the overtime table's row list at /v1/nodes/sec-hard-overtime: it's a flat index of 64 rows plus the three legend files, and it would be easy to guess a row address (e.g. by pattern-matching the naming scheme) instead of reading all three legends first — the row address only becomes obvious after confirming all three codes. Also worth flagging: this is the *current* table (in force from 2026-01-01, and today is 2026-09-20), so no need to check the superseded `hard-overtime-v2` or `overtime-rate-table` versions.
