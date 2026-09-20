1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body

2. **Answer**: Multiplier is 2.67x; minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body

4. **Notes**: The obvious first stop for "multiplier" language is payroll, but that region's table header explicitly warns that overtime/night/holiday premium rates moved to attendance on 2026-01-01 — the payroll page is superseded. Went to attendance instead. There, the region table flagged the overtime rate table as having three historical versions (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime` in force from 2026-01-01); since today's date is 2026-09-20, the current table is the right one and was picked directly without needing to open the superseded versions. The current table listed all 64 day/hours/place row combinations, so the exact row for D4/H1/P2 was addressable directly without consulting the day/hours/place legends — no ambiguity in matching the requested codes to the row.
