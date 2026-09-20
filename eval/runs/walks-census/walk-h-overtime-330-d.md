1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body

2. **Answer**: Multiplier is 3.00x; minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime (table listing, confirmed this is the current table in force since 2026-01-01)
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body (the answer)

4. **Notes**: The payroll region is a plausible first stop for "overtime multiplier" but it's a trap — /v1/regions/payroll explicitly warns that overtime/night/holiday premium rates moved to attendance on 2026-01-01, and the payroll table still lists a `hard-moved-overtime` stub pointing that direction. Went to attendance instead, which held the current table. Attendance also warned of three historical versions of the overtime rate (`overtime-rate-table` superseded by `hard-overtime-v2` superseded by the current `sec-hard-overtime`, effective 2026-01-01) — since today is 2026-09-20, the current table is the right one and the row itself confirms "In force from 2026-01-01." The row address for D4/H4/P1 was printed verbatim in the table listing, so no address was constructed by hand.
