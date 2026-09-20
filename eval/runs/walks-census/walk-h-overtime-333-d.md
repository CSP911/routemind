1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p4/body

2. **Answer**: Multiplier 3.09x; minutes rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p4/body

4. **Notes**: The overtime rate used to live under payroll, but that region's table flags (via `hard-moved-overtime`) that overtime premiums moved to attendance on 2026-01-01 — following payroll straight to a rate table there would have given a superseded answer. Attendance itself also holds two older overtime tables (`hard-overtime-v2` covering 2024-07-01 to 2025-12-31, and the original `overtime-rate-table`) alongside the current one, `sec-hard-overtime` (in force from 2026-01-01); today's date of 2026-09-20 falls under the current table, so no disambiguation of which version applies was needed here, but it would be easy to grab a superseded row by accident. The D4/H4/P4 row address followed the table's printed naming pattern exactly, so no guessing was required.
