1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H4, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime rules likely live under attendance" --member /v1/regions/payroll "overtime multiplier/pay is a payroll concept"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f63798 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body

2. **Answer**: Multiplier is 1.65x. Minutes are rounded to the nearest 20 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate table versions is current as of today, 2026-09-20)
- /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body (the row with the multiplier and rounding rule)

4. **Notes**: The question gives coded qualifiers (D1/H4/P4) but no explicit date, and the overtime rate subject has three superseded/current versions covering different date ranges (until 2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), with the warning that the oldest version says nothing about being replaced — so grabbing the first hit without checking the legend-revision page could silently give a stale multiplier. Since today's date is 2026-09-20, the current table (`sec-hard-overtime`, in force from 2026-01-01) is the right one, and it happened to contain an exact-match row for D1/H4/P4, so no legend lookups for day/hours/place codes were needed. Payroll region was pulled into the initial overlay on the assumption overtime pay might be documented there, but a note on that region's `hard-moved-overtime` page indicates overtime premiums moved to attendance on 2026-01-01, confirming attendance was the right region and payroll was a dead end.
