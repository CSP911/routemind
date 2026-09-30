1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "An ordinary tuesday, about ninety minutes, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier likely a payroll pay-rate topic" --member /v1/regions/attendance "overtime/desk time could be an attendance-tracking rule"
./bench/rmcli.py overlay remove --id ov_2026-09-20_321afe --address /v1/nodes/insurance --why "not overtime related"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_321afe --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body

2. **Answer**
Multiplier: 1.20x. Rounding: to the nearest 5 minutes.
(An ordinary Tuesday = day D1, about ninety minutes = hours H1, at my desk = place P1 — current table, in force from 2026-01-01.)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body

4. **Notes**
The overlay I created up front (rows from /v1/regions/payroll and /v1/regions/attendance) turned out to be too broad — the payroll region actually warns overtime premiums moved to attendance on 2026-01-01, so most of the payroll candidates were dead ends and only the attendance-side "overtime" nodes mattered. The real risk in this walk was the date-versioning trap: `hard-overtime-legend-revision` warns there are THREE versions of the overtime rate table (pre-2024-07-01, 2024-07-01–2025-12-31 as `hard-overtime-v2`, and current `sec-hard-overtime` from 2026-01-01), and explicitly says reaching for the newest is wrong for dates before 2026-01-01. Since today is 2026-09-20/21, the current table was correct here, but I made a point of reading that warning file before picking a version rather than assuming. Also note the three legend files (day/hours/place) had to be read in full to translate "an ordinary Tuesday," "about ninety minutes," and "at my desk" into the D1/H1/P1 codes that index the row table — the row table itself never spells out the plain-language meaning of its own codes, only the legends do. The overlay's "reached = answered from somewhere the overlay never named" note on close is because I read the legend and row files directly via `table`/`read` rather than adding each as an explicit overlay member first; that's just an artifact of my navigation, not a gap in the answer.
