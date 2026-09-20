1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body

2. **Answer**: Multiplier is 2.76x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body

4. **Notes**: The obvious first stop was payroll (overtime sounds like a payroll topic), but its table page flags up front that overtime premiums moved to attendance on 2026-01-01, so payroll only serves as a redirect — reading past that header would have wasted a step. The attendance area then has both a current overtime table (`sec-hard-overtime`, in force since 2026-01-01) and old superseded versions (`hard-overtime-v2`, `overtime-rate-table`) sitting in the same listing; picking the current one required reading the "WHY YOU WOULD PICK THIS ROW" text carefully rather than grabbing the first "overtime" match. Once inside `sec-hard-overtime`, the table is pre-indexed by day/hours/place code (64 rows), so the D4/H2/P1 row address could be read off the listing directly without needing the legend files — no ambiguity there.