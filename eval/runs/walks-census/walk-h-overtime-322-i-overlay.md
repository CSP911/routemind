1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, six hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime/standby multiplier and minute rounding likely defined in payroll rules" --member /v1/regions/attendance "standby/on-call time tracking may be defined in attendance rules"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_05cf8c --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body

2. **Answer**: Multiplier 2.94x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body

4. **Notes**: The top-level table listed neither "overtime" nor "standby" directly — I had to infer from the payroll and attendance row descriptions that overtime rules would be there, and picked both as members since a stale warning (`hard-moved-overtime`) said overtime premiums had moved from payroll to attendance on 2026-01-01. The actual current table, `sec-hard-overtime`, lives under attendance, confirming that move. The three qualifiers ("two in the morning" → day D4, "six hours" → hours H3, "on standby at home" → place P3) each required reading a separate legend document before the row address could be built — none of these codes are guessable, and getting any one wrong (e.g. confusing "on standby at home" P3 with the very similarly worded "from home" P4) would have silently produced a different, wrong row. I double-checked the row's "In force from 2026-01-01" date against today (2026-09-21) to confirm it's the current version and not one of the two superseded tables (`hard-overtime-v2`, `overtime-rate-table`) also present in the corpus. The overlay close reported the four addresses I used as "reached" rather than as pre-declared members, since I had only added the two top-level region tables as members, not the leaf documents themselves — the tool still recorded them correctly against my `--used` list.
