1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H3, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding are payroll topics"
./bench/rmcli.py overlay add --id ov_2026-09-20_101842 --address /v1/regions/attendance --why "overtime moved-notice says overtime premiums are now set in attendance's sec-hard-overtime table"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_101842 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body

2. **Answer**: Multiplier is 1.44x. Minutes are rounded to the nearest 15 minutes. (This is the current table, in force from 2026-01-01 onward; no approval needed in advance, and it counts toward the monthly cap.)

3. **Source**:
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body

4. **Notes**: My first instinct was to open the payroll region, since "multiplier" and "rounding" sound like payroll mechanics — but payroll's own overlay row carried a WARNING body (`hard-moved-overtime`) saying overtime premiums moved to attendance's `sec-hard-overtime` as of 2026-01-01, and the old payroll page (`payslip-overtime`) is only correct before that date. That would have been a wrong-region answer if I'd skipped it. Attendance also turned out to have a second trap: `hard-overtime-legend-revision` shows the "overtime rate" topic has been written three separate times (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and the two older versions never say they were superseded. The question gives three qualifiers (D1/H3/P1), which only the current table (`sec-hard-overtime`) is indexed by, and today's date (2026-09-20/21) is well after 2026-01-01, so the current table was the right pick — but nothing forced that conclusion automatically; a careless reader could have grabbed `overtime-rate-table` or `hard-overtime-v2` by mistake since both still exist and look plausible. Once in `sec-hard-overtime`, the row for D1/H3/P1 was listed explicitly and unambiguously.
