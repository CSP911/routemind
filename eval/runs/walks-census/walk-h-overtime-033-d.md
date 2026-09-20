1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body

2. **Answer**: For day D1, hours H4, place P4: multiplier is 1.65x; minutes are rounded to the nearest 20 minutes. (This row is in force from 2026-01-01, current as of today 2026-09-20.)

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body

4. **Notes**: The path was direct — /v1/regions/attendance's row for `sec-hard-overtime` was explicitly labeled "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," which made it easy to distinguish from the superseded `hard-overtime-v2` and `overtime-rate-table` entries listed alongside it. The row table itself is a flat 64-row index by day/hours/place code, and the exact address `hard-overtime-row-day-d1-hours-h4-place-p4` matched the requested D1/H4/P4 combination verbatim, so no legend lookup (day/hours/place code definitions) was needed to resolve which row applied. The only thing worth flagging: I did not open the legend files (`hard-overtime-legend-day/hours/place`) to independently verify what D1/H4/P4 *mean*, since the question gave the codes directly rather than plain-language conditions — if the codes in the question didn't already match RouteMind's coding scheme, this answer could be silently wrong. Given the question phrased the query already in D1/H4/P4 form, this seemed safe to skip.
