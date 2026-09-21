1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H3, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding sound like payroll pay-rate rules" --member /v1/regions/attendance "day/hours/place could be attendance overtime request classification"
./bench/rmcli.py overlay remove --id ov_2026-09-20_543860 --address /v1/nodes/insurance --why "not related to overtime multiplier"
./bench/rmcli.py overlay add --id ov_2026-09-20_543860 --address /v1/nodes/sec-hard-overtime --why "current overtime rate table by day, hours, place - directly matches question"
./bench/rmcli.py overlay add --id ov_2026-09-20_543860 --address /v1/nodes/hard-overtime-legend-revision/body --why "warns overtime rate has three versions with different date ranges - must confirm which applies for 2026-09-20"
./bench/rmcli.py overlay add --id ov_2026-09-20_543860 --address /v1/nodes/hard-moved-overtime/body --why "warns overtime premiums moved from payroll to attendance on 2026-01-01 - confirms right region"
./bench/rmcli.py overlay remove --id ov_2026-09-20_543860 --address /v1/regions/payroll --why "overtime now lives in attendance per hard-moved-overtime warning"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_543860 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-moved-overtime/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body

2. **Answer**: Multiplier 1.92x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body

4. **Notes**: The first guess (payroll) was a plausible trap — overtime multipliers sound like a pay-rate question, but `hard-moved-overtime/body` explicitly says overtime premiums moved out of payroll into attendance as of 2026-01-01, and payroll's own `payslip-overtime` line is now stale for any date on/after that. Separately, `hard-overtime-legend-revision/body` warns this same subject has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward) and that the oldest version says nothing about being superseded — so blindly opening the first "overtime" hit without checking the revision-legend page would have risked reading a withdrawn-in-effect table. Since the question gives no date but today (2026-09-20) is well past 2026-01-01, the current table `sec-hard-overtime` is correct. Also worth flagging: adding specific row/table addresses as overlay members caused the overlay to balloon (38 → 105 rows) because each added table member gets expanded into its own child rows — I stopped fighting the overlay tool and just read the needed documents directly instead, which is why the closing row `hard-overtime-row-day-d2-hours-h3-place-p1/body` shows as "reached" rather than a formal member.
