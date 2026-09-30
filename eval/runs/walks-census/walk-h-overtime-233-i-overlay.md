1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, eleven hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime/holiday pay multipliers usually documented under payroll" --member /v1/regions/attendance "holiday work and remote/from-home hours logging usually documented under attendance"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6ba49d --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body

2. **Answer**: Multiplier 2.61x; minutes are rounded to the nearest 20 minutes. (This is from the current overtime rate table, in force since 2026-01-01, which applies as of today 2026-09-21.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (eleven hours → hours H4)
- /v1/nodes/hard-overtime-legend-place/body (from home → place P4)
- /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body (2.61x multiplier, rounding to the nearest 20 minutes)

4. **Notes**: The row addresses (day-D3-hours-H4-place-P4) can't be built directly from the question's words — each of the three qualifiers ("Liberation day", "eleven hours", "from home") has to be translated separately through its own legend document before the actual row address is known, and the legends explicitly warn they are "the only place the mapping is written down." It would have been easy to skip straight to guessing a row address; the legends made clear that's not permitted. Also worth flagging: the attendance region carries a warning file (`hard-moved-overtime/body`, surfaced under the payroll branch of the working set) saying overtime premiums moved from payroll to attendance on 2026-01-01 — and the table itself carries superseded versions (`hard-overtime-v2` for 2024-07-01–2025-12-31, `overtime-rate-table` before that) alongside the current one. Since today is 2026-09-21, the current table (`sec-hard-overtime`, in force from 2026-01-01) is the correct one, but a walk done without checking effective dates could easily have pulled a stale multiplier from an older version.
