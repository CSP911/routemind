1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body

2. **Answer**: Multiplier is 2.97x; minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body

4. **Notes**: The attendance area's table listing flags that the overtime rate table has THREE versions with different rates, and calls out a legend-revision warning document (`hard-overtime-legend-revision`) plus a superseded version (`hard-overtime-v2`) right alongside the current one — easy to grab the wrong version if you don't check dates. `/v1/nodes/sec-hard-overtime` is explicitly labeled "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," which matches today's date (2026-09-20), so this is the correct version and no need to consult the superseded ones. The row address matched the D4/H3/P4 qualifiers exactly as printed, so no legend lookups for day/hours/place codes were needed — the question already used the table's own coding.
