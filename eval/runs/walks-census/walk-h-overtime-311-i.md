1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body

2. **Answer**: Multiplier 2.79x; minutes rounded to the nearest 10 minutes.

3. **Source**:
/v1/regions/payroll (pointed away — overtime moved to attendance on 2026-01-01)
/v1/regions/attendance
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body

4. **Notes**: The obvious first stop, payroll, is a trap — it explicitly warns overtime premiums moved to attendance on 2026-01-01, so I had to redirect there. The bigger trap is the day legend: "two in the morning" is not an hours-band entry, it's a *day-type* code (D4), sitting in the same table as "an ordinary Tuesday" and "Liberation Day." It would be easy to assume the day code defaults to D1 (ordinary day) since the question gives no calendar date, and instead go hunting for "2am" in the hours legend — but the hours legend only bands *durations* ("about ninety minutes," "three hours," etc.), not clock times. "Three hours" maps cleanly to H2, and "out at a client's office" to P2, giving row D4/H2/P2 with no ambiguity once the day legend is read correctly. I did not need to consult the superseded hard-overtime-v2/legend-revision files since the question gives no date requiring the older rate, and today (2026-09-20) falls under the current table (in force since 2026-01-01).
