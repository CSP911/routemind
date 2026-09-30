1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body
./bench/rmcli.py overlay create --question "For day D1, hours H2, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body "exact row for D1/H2/P2 in the current overtime table"
./bench/rmcli.py overlay close --id ov_2026-09-20_4f1292 --outcome answered --used /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body

2. **Answer**: Multiplier is 1.35x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body

4. **Notes**: Straightforward walk — the table at /v1/nodes/sec-hard-overtime is indexed directly by day/hours/place code, so the row address for D1/H2/P2 could be read off the table listing without guessing. No ambiguity: this is the current table (in force from 2026-01-01), not one of the two superseded versions (hard-overtime-v2, overtime-rate-table) also visible in the attendance area — worth double-checking the "in force" note on the row itself, which confirmed it matched the current version.
