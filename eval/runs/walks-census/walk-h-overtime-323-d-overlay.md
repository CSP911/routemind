1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D4, hours H3, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers/pay rates are typically documented under payroll" --member /v1/regions/attendance "attendance rules may define overtime hour codes and rounding"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_929b80 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body

2. **Answer**: Multiplier 2.97x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body

4. **Notes**: The overtime area has three superseded versions of the same table (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime` from 2026-01-01), and a warning node (`hard-overtime-legend-revision`) explicitly says reaching for the newest is wrong for a question dated before 2026-01-01 — the oldest version doesn't even say it was replaced. Today's date (2026-09-21) is well inside the current table's range, so `sec-hard-overtime` was correct, but this is exactly the trap the walk was built to catch: I confirmed the date-to-version mapping before reading the row rather than assuming "current" was right. There's also a payroll-side warning node (`hard-moved-overtime`) noting overtime premiums moved out of payroll into attendance on 2026-01-01 — consistent with finding the real table under attendance, not payroll, despite the question sounding like a pay-rate question. Once the correct table was found, the day/hours/place row was listed directly (`hard-overtime-row-day-d4-hours-h3-place-p4`), so no legend lookups for D4/H3/P4 codes were needed.
