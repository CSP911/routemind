1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body

2. **Answer**: Multiplier is 2.85x; minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body

4. **Notes**: The walk was straightforward — the attendance area table clearly marked `/v1/nodes/sec-hard-overtime` as "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," which matches today's date (2026-09-20), so there was no need to consult the superseded `hard-overtime-v2` or `overtime-rate-table` versions. The row address itself directly encoded day D4/hours H2/place P4, so no legend lookup (day/hours/place legends) was needed since the question already gave the codes rather than raw descriptions — had it given plain-language day/hour/place descriptions instead of codes, the legend files (`hard-overtime-legend-day`, `hard-overtime-legend-hours`, `hard-overtime-legend-place`) would have been necessary first to map them to D/H/P codes.
