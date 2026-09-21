1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, six hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding are payroll pay-rate concepts" --member /v1/regions/attendance "attendance may define remote/home work and time tracking rounding rules"
./bench/rmcli.py read /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_7038ea --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body

2. **Answer**
Multiplier: 2.97x. Rounding: to the nearest 15 minutes.
(Row: day D4, hours H3, place P4 — from the current overtime rate table, in force from 2026-01-01. Approval was needed in advance for this row, and it counts toward the monthly cap.)

3. **Source**
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body

4. **Notes**
The three qualifiers in the question don't map onto the row axes the way plain English suggests. "Two in the morning" sounds like it should feed the hours legend, but the *day* legend is the one that claims it ("two in the morning → day D4") — the hours legend is instead banded by duration ("six hours → hours H3"). If I'd assumed "two in the morning" was about hours worked and tried to guess a day code from context (e.g. treating it as an ordinary weekday, D1), I'd have picked the wrong row entirely. The payroll region's own table pointed away from itself first: it carries a hard-moved-overtime warning saying overtime premiums moved to attendance on 2026-01-01, and the actual current table (sec-hard-overtime, in force from 2026-01-01) lives under /v1/regions/attendance, not payroll — so starting the overlay with payroll as the leading guess wasn't wrong, but the real answer sat in the sibling region. Also worth flagging: there are three superseded versions of this table (hard-overtime-v2, overtime-rate-table, plus the current one), so checking that "in force from 2026-01-01" still covers today (2026-09-21) was necessary, not optional.
