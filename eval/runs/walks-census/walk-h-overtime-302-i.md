1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body

2. **Answer**: Multiplier 2.70x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/regions/payroll (routed away — overtime moved to attendance on 2026-01-01)
/v1/nodes/sec-hard-overtime (current overtime rate table)
/v1/nodes/hard-overtime-legend-day/body (maps "two in the morning" → day D4)
/v1/nodes/hard-overtime-legend-hours/body (maps "about ninety minutes" → hours H1)
/v1/nodes/hard-overtime-legend-place/body (maps "on standby at home" → place P3)
/v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body (the answer row)

4. **Notes**: The payroll area looked like the natural place for a "multiplier" question, but its overtime page is explicitly marked superseded — a banner says the rates moved to attendance on 2026-01-01, which is the current date, so that move applies. Easy to go wrong here by reading the old payroll page instead of following the pointer.

The bigger trap is the day legend: "two in the morning" is listed as a day type (D4), not a time-of-day modifier layered on top of an ordinary weekday. It's tempting to think "2am on some unspecified day" needs a separate day code plus a night-hours flag, but the legend treats "two in the morning" itself as the whole day classification — there's no separate weekday/night combination in this scheme. Once that's accepted, the other two axes (duration → H1, location → P3) map directly and unambiguously, and the row lookup is exact, not a nearest-match guess.
