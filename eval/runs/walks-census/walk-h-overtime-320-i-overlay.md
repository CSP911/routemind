1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "Two in the morning, six hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/night premium rates moved here from payroll on 2026-01-01, per payroll table note"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a27237 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body

2. **Answer**: Multiplier 2.88x; minutes rounded to the nearest 15 minutes. (Current table, in force from 2026-01-01; approval was needed in advance and the hours count toward the monthly cap.)

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body

4. **Notes**: The payroll region's table flags up front that overtime/night premiums moved to attendance on 2026-01-01, so the payroll-side "old rule" page (hard-moved-overtime) was a dead end I skipped rather than walked into. The bigger trap was the day legend: "day D4" is not a weekday/weekend/holiday category like D1–D3, it is literally "two in the morning" — a time-of-day case slipped into what looks like a day-type axis. Easy to misread the row index as (weekday-type, hours-band, place) and go hunting for which weekday "two in the morning" falls on; the legend table resolves it directly to D4 with no date needed. Hours ("six hours") and place ("at my desk") legends mapped cleanly to H3 and P1 with no ambiguity. Only one candidate row existed for D4×H3×P1, so no version-conflict to resolve — the row itself confirms it's the current (2026-01-01-forward) figure, with pointers to the two older superseded versions I didn't need.