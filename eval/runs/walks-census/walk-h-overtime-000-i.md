1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body

2. **Answer**: Multiplier 1.20x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-moved-overtime/body (confirms overtime moved from payroll to attendance as of 2026-01-01)
/v1/nodes/hard-overtime-legend-revision/body (confirms which of three versions applies for today's date, 2026-09-20)
/v1/nodes/hard-overtime-legend-day/body (an ordinary Tuesday → day D1)
/v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
/v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body (multiplier and rounding for D1/H1/P1)

4. **Notes**: The question starts in payroll — payslip line language ("what multiplier applies") naturally points there — but payroll's own table flags that overtime premiums moved to attendance on 2026-01-01, and the old payroll page is only correct for dates before that. That was the first near-miss: reading the payslip-overtime table in payroll would have given a stale answer. The second near-miss is the three-version trap in attendance itself (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) — reaching for the newest without checking the date, or for the oldest since it "says nothing about being replaced," are both explicitly called out as wrong; today's date (2026-09-20) falls after 2026-01-01 so the current table (`sec-hard-overtime`) is correct. Finally, the row table is indexed by three codes (day/hours/place) that must be looked up individually in three separate legend files rather than guessed — "ninety minutes" only resolves to H1 via the hours legend, not by any arithmetic.
