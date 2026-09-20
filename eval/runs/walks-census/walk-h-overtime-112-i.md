1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body

2. **Answer**: Multiplier 1.86x; minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body

4. **Notes**: The table at /v1/nodes/sec-hard-overtime is indexed by opaque codes (D1–D4, H1–H4, P1–P4), and the row list gives no clue what those codes mean — you have to detour through three separate legend files (day, hours, place) to translate "a Saturday" → D2, "three hours" → H2, and "on standby at home" → P3 before you can even pick the right row out of 64. Skipping any one of the three legends would have made it easy to grab a plausible-looking but wrong row (e.g. confusing "on standby at home" with "from home", which is a different place code, P4, with presumably a different multiplier). The attendance area also listed two superseded overtime tables (hard-overtime-v2 and a legend-revision warning file) alongside the current one — worth noting because it would be easy to accidentally read a superseded table's row instead of the one in force since 2026-01-01 (sec-hard-overtime), which is the one that covers today's date, 2026-09-20. I didn't need to open the revision-warning file since the region table already flagged sec-hard-overtime as "current."
