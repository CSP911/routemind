1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body
./bench/rmcli.py overlay create --question "For day D3, hours H3, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body "exact row matching D3/H3/P4 in the current overtime rate table"
./bench/rmcli.py overlay close --id ov_2026-09-21_5b3553 --outcome answered --used /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body

2. **Answer**: Multiplier is 2.49x. Minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body

4. **Notes**: The attendance area table flagged up front that there are three historical versions of the overtime rate rules (`overtime-rate-table`, then `hard-overtime-v2` for 2024-07-01 to 2025-12-31, then the current one), and payroll's own table has a big warning that overtime premiums moved out of payroll entirely on 2026-01-01. It would have been easy to grab a superseded row or answer from the payroll side out of habit. I went straight to `/v1/nodes/sec-hard-overtime`, confirmed it's marked as the table "in force from 2026-01-01" (current for today's date), and read the row addressed exactly by day/hours/place code D3/H3/P4 rather than any of the D1/D2/D4 or other hours/place variants sitting next to it in the listing — the address naming convention made picking the exact row unambiguous once I knew the codes matched literally.
