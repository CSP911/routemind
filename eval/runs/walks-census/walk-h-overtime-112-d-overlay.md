1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py overlay create --question "For day D2, hours H2, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body "The exact row for D2/H2/P3 in the current (2026-01-01+) overtime table"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_849213 --outcome answered --used /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body

2. **Answer**: Multiplier is 1.86x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body

4. **Notes**: My first instinct was to look in payroll, since "overtime" sounds like a payroll topic — but the payroll region's table page explicitly flags that overtime, night and holiday premium rates moved to attendance on 2026-01-01, with the old payroll page superseded. That warning caught me before I read the wrong (stale) figure. Attendance's own table then repeats the same kind of warning for its own overtime pages: there are three historical versions (`overtime-rate-table`, `hard-overtime-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-overtime` in force from 2026-01-01), and today's date (2026-09-20) put me squarely in the current version's window, so I went straight to `sec-hard-overtime` rather than the superseded ones. Inside that table, D2/H2/P3 is a single exact row (out of 64 day×hours×place combinations), so no interpretation was needed — I just read it directly. No genuine ambiguity in the end, but the overlapping "moved to attendance" and "three versions" warnings were exactly the kind of trap that could lead to citing a stale rate if skipped.
