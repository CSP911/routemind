1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "For day D4, hours H2, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/night/holiday premium rates moved here from payroll on 2026-01-01 per payroll page note"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_974901 --outcome answered --used /v1/regions/payroll /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body

2. **Answer**: Multiplier 2.79x. Rounding: to the nearest 10 minutes.

3. **Source**:
- /v1/regions/payroll (found the warning that overtime rates moved to attendance on 2026-01-01)
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions applies to today's date)
- /v1/nodes/sec-hard-overtime (the current overtime rate table, in force from 2026-01-01)
- /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body (the row with the actual figures)

4. **Notes**: The payroll area is a trap for this question — it's the first place you'd naturally look for anything payslip/overtime-related, but its own page warns that overtime premiums moved to attendance on 2026-01-01 and that the payroll copy is stale. Attendance holds three separate overtime-rate documents (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) covering different date ranges, with no marking on the oldest one to say it's superseded — the legend-revision doc is the only thing that tells you which one is current for today's date (2026-09-20/21 → `sec-hard-overtime`, in force from 2026-01-01). Picking the newest table without checking the date would happen to be right here, but only by luck — the revision doc explicitly warns that assuming "newest wins" is wrong for anything dated in 2025. The day/hours/place codes (D4/H2/P2) were already given as codes in the question, so I didn't need the legends to translate anything, but I read them anyway to confirm D4/H2/P2 are valid codes and not something I was meant to derive from a description.
