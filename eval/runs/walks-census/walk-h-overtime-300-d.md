1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body

2. **Answer**: Multiplier is 2.64x. Minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body

4. **Notes**: Started at /v1/regions/payroll since overtime pay sounds like a payroll question, but that area's own table header flagged that overtime/night/holiday premium rates moved to attendance on 2026-01-01 and the payroll page is now the superseded old rule — that redirect saved a wrong answer. In /v1/regions/attendance there are two overtime tables: the current one (`sec-hard-overtime`, in force since 2026-01-01) and a superseded one (`hard-overtime-v2`, 2024-07-01 to 2025-12-31), plus a legend-revision warning file. Since today's date is 2026-09-20, the current table applies, and the row address for D4/H1/P1 was printed directly by the table listing, so no guessing of the address was needed.
