1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body

2. **Answer**: Multiplier 2.64x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body

4. **Notes**: The overtime rate table has three superseded versions; the legend-revision page warns not to assume the newest applies to old dates, but since today is 2026-09-20 the current table (`sec-hard-overtime`, in force since 2026-01-01) is correct here without any adjustment. The real trap is the day legend: "two in the morning" is not an hours qualifier at all — it maps to a *day* code (D4), sitting in the same table as "an ordinary Tuesday" and "a Saturday." It would be easy to read "two in the morning" as describing when the work happened within a shift and go hunting for it in the hours-band legend instead, or to assume the day code should be "ordinary day" (D1) since the question doesn't mention a weekend or holiday. The hours qualifier actually comes from "about ninety minutes" (H1), and place comes from "at my desk" (P1). All three legends explicitly say to take the nearest entry if a value isn't listed verbatim, but here all three had exact matches.
