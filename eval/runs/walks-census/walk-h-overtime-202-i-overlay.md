1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, about ninety minutes, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "holiday standby / overtime rules likely live under attendance" --member /v1/regions/payroll "overtime multiplier and rounding of minutes could be a payroll rule"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a5c748 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body

2. **Answer**: Multiplier 2.22x; minutes rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body

4. **Notes**: The overtime table is qualified by three legends (day, hours, place) that must each be resolved before the row address can be built: "Liberation Day" → day D3, "about ninety minutes" → hours H1, "on standby at home" → place P3, giving row day-d3-hours-h1-place-p3. The revision-warning file flagged that overtime rates have three versions across different date ranges; since the question gave no specific calendar date and today is 2026-09-21, the current table (`sec-hard-overtime`, in force from 2026-01-01) was the right one — the older `hard-overtime-v2` and `overtime-rate-table` versions were not consulted since nothing pointed to a pre-2026 date. One thing worth flagging: my overlay members were the two top-level region tables (attendance, payroll), not the specific leaf files I ended up reading — the overlay close command reported the five addresses I passed to `--used` as "reached" rather than as members that had been added to the working set, since I never formally added them via `overlay add`. The answer itself is unaffected, but a stricter reading of "keep a working set" would have had me `add` each leaf address (with its reason) before closing.
