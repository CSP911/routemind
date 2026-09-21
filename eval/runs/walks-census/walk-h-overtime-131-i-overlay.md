1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, 11 hours, at a client's office: what multiplier applies, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/hours worked rules likely live here" --member /v1/regions/payroll "overtime pay multiplier likely defined in payroll"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_238ded --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body

2. **Answer**: Multiplier 2.07x; minutes rounded to the nearest 20 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
- /v1/nodes/hard-overtime-legend-hours/body (eleven hours → hours H4)
- /v1/nodes/hard-overtime-legend-place/body (out at a client's office → place P2)
- /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body (the row: multiplier 2.07x, rounding to the nearest 20 minutes)

4. **Notes**: The overtime table has three superseded versions (`overtime-rate-table`, then `hard-overtime-v2` for 2024-07-01 to 2025-12-31); a warning node (`hard-overtime-legend-revision`) flags this explicitly. Today is 2026-09-21, so the current table `sec-hard-overtime`, in force from 2026-01-01, is the right one — I confirmed the row's own "in force from 2026-01-01" footer before using it, which is what kept me from accidentally pulling a stale rate. The three qualifiers (day/hours/place) each needed their own legend lookup before the row address could be assembled — the legends explicitly state they are "the only place the mapping is written down," so guessing the code letters from the wording alone would have been a mistake even though the mapping seemed intuitive (Saturday=D2, out at client's office=P2). The payroll region turned out to be a dead end for this question: `hard-moved-overtime` there just points back to attendance, confirming the attendance region was the right pick, not a wasted detour.
