1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body

2. **Answer**: Multiplier 2.82x. Minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body

4. **Notes**: Overtime premiums used to live in payroll (`payslip-overtime`), but a warning node there (`hard-moved-overtime`) says they moved to attendance's `sec-hard-overtime` table effective 2026-01-01, which covers today's date (2026-09-20) — the payroll page is stale and would have given the wrong table entirely if I'd stopped there. The bigger trap was the day legend: "two in the morning" is not an hours code, it's a **day** code (D4) — a separate, disjoint dimension from the hours-worked code (H2, "three hours") and the place code (P3, "standby at home"). It would be easy to misread "two in the morning" as describing when the shift started and try to fold it into the hours band, or to skip the day legend altogether since the question doesn't mention a weekday. The legend table is explicit that D4 literally means "two in the morning," so the three qualifiers (day, hours, place) are independent axes that all had to be resolved separately before the row address could be built.