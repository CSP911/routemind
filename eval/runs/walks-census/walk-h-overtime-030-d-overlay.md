1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "For day D1, hours H4, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a29d73 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body

2. **Answer**:
Multiplier: 1.56x. Rounding: to the nearest 20 minutes. (In force from 2026-01-01; approval needed in advance; counts toward the monthly cap.)

3. **Source**:
/v1/nodes/sec-hard-overtime (table, to locate the row)
/v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body (the row with the figures)

4. **Notes**:
Payroll's area listing flagged that overtime premiums moved to attendance on 2026-01-01 (`/v1/nodes/hard-moved-overtime/body`), which confirmed attendance was the right region before I opened it — worth checking since payroll would otherwise look like a plausible first guess for "multiplier." The overtime table also has two superseded versions (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and `overtime-rate-table` before that); I only used the current table (`sec-hard-overtime`, in force since 2026-01-01) since the question gave no date, and today's date is 2026-09-20/21. The row I needed (D1/H4/P1) was printed directly by the table listing with its exact address, so no legend lookups were needed to translate day/hours/place codes. The overlay's close output noted the row address was "reached" rather than a named member, since I'd only added the parent table to the working set, not the individual row — harmless, but worth flagging as a quirk of how overlay membership is tracked.
