1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body

2. Answer
Multiplier: 1.98x
Rounding: to the nearest 15 minutes

3. Source
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body

4. Notes
The first instinct was to answer from payroll, since that's the natural place to look for pay
multipliers — but payroll's table page carries an explicit warning that overtime premiums moved to
attendance on 2026-01-01, and today's date (2026-09-20) is after that cutover, so the payroll page
(`payslip-overtime`) would have given a stale/wrong answer. The current table lives in attendance at
`sec-hard-overtime`, which is indexed by three independently-coded axes (day/hours/place) rather than
by plain English, so each of "a Saturday," "six hours," and "on standby at home" had to be translated
through its own legend table before the right row (D2/H3/P3) could be addressed. Attendance also has
superseded overtime pages (`hard-overtime-v2`, `overtime-rate-table`) sitting alongside the current
one with similar names — easy to grab the wrong one if not reading the "in force from" note on the
row itself, which I did check.
