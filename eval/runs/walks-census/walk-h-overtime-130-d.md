1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body

2. **Answer**
Multiplier: 2.04x. Rounding: minutes are rounded to the nearest 20 minutes.

3. **Source**
/v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body

4. **Notes**
The table root has an `attendance` area whose description mentions overtime by day type, hours,
and place directly, so the path to `/v1/nodes/sec-hard-overtime` was unambiguous. Inside that
node there are three superseded/legend siblings (`hard-overtime-v2`, `hard-overtime-legend-revision`,
etc.) that could have led to an out-of-date multiplier if picked instead of
`sec-hard-overtime` — the listing explicitly flags `sec-hard-overtime` as "THE CURRENT OVERTIME
RATE TABLE, in force from 2026-01-01," which matches today's date (2026-09-20), so no version
check against the legend-revision doc was needed beyond confirming that label. The row address
for D2/H4/P1 was printed verbatim in the table listing and matched exactly, so no address was
constructed by hand.
