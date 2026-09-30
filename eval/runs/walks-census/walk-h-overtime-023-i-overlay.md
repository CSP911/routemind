1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "An ordinary tuesday, six hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and rounding likely defined here" --member /v1/regions/attendance "work-from-home ordinary day overtime rules might be defined here"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay close --id ov_2026-09-20_ccc326 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body

2. **Answer**: Multiplier 1.53x; minutes rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (established today's date, 2026-09-20, falls under the current table, not the two superseded versions)
- /v1/nodes/hard-overtime-legend-day/body (an ordinary Tuesday → day D1)
- /v1/nodes/hard-overtime-legend-hours/body (six hours → hours H3)
- /v1/nodes/hard-overtime-legend-place/body (from home → place P4)
- /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body (the row: multiplier 1.53x, rounding to the nearest 15 minutes)

4. **Notes**: The overtime rules have moved and forked twice — payroll's own `hard-moved-overtime` warning says overtime premiums left payroll for attendance on 2026-01-01, and attendance's `hard-overtime-legend-revision` warns of three versions of the overtime table with different date ranges, indexed by one, two, then three qualifiers respectively. It would have been easy to land on the payroll region (since "multiplier" sounds like a pay calculation) and either read the stale `payslip-overtime` line or miss the version-currency check entirely. Because today's date (2026-09-20) postdates 2026-01-01, the current three-qualifier table `sec-hard-overtime` applies, not `hard-overtime-v2`. The three legends translate the plain-English phrasing exactly ("an ordinary Tuesday" = D1, "six hours" = H3, "from home" = P4) without needing interpretation — the only place a wrong guess was plausible was skipping the date-currency check and jumping straight to `hard-overtime-v2` out of habit or without reading the revision-legend warning first.
