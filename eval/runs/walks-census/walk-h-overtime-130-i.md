1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body

2. Answer:
Multiplier: 2.04x. Rounding: to the nearest 20 minutes.

3. Source:
/v1/nodes/hard-overtime-legend-revision/body (confirmed 2026-09-20 falls under the current, 2026-01-01-onwards table)
/v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
/v1/nodes/hard-overtime-legend-hours/body (eleven hours → hours H4)
/v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
/v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body (the answer: 2.04x, nearest 20 minutes)

4. Notes:
Payroll's own table looked like the natural first stop (it lists payslip lines and rates), but its
top-level entry explicitly warns that overtime/night/holiday premiums moved to attendance on
2026-01-01 — going by the payroll page alone would have been wrong. Attendance then has three
superseded versions of the overtime table (pre-2024-07-01, 2024-07-01–2025-12-31, and
2026-01-01-onwards); the legend-revision file is explicit that the oldest version carries no notice
of being replaced, so skipping that check and reading the first table found would risk citing a
stale rate. Today's date (2026-09-20) sits in the current range, so `sec-hard-overtime` was the
right table. The three qualifiers (day/hours/place) each needed their own legend lookup since the
row addresses are coded (d2/h4/p1) rather than in plain language — "Saturday", "eleven hours", and
"at my desk" each map to an exact legend entry, not an approximation, so no rounding-to-nearest-entry
judgment call was needed here.
