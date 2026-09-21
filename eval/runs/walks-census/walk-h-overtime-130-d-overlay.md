1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H4, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multipliers and minute rounding are attendance-related pay rules"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3113f1 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body

2. **Answer**: Multiplier 2.04x; minutes are rounded to the nearest 20 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body
- /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body

4. **Notes**: The overtime rate subject has three versions in force over different date ranges (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend-revision doc warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-21) falls in the current version's range, so `sec-hard-overtime` was the correct table — but this was a real branch point worth checking rather than assuming. The current table's row list is indexed by exactly day+hours+place (e.g. `hard-overtime-row-day-d2-hours-h4-place-p1`), so once the qualifiers D2/H4/P1 were known the row address could be picked straight off the table listing without needing the day/hours/place legend docs at all.
