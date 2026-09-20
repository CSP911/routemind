1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body

2. **Answer**: Multiplier is 2.73x. Minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body

4. **Notes**: The first instinct was to look under payroll (payslip lines, overtime rates historically lived there), but the payroll table itself carries a warning that overtime, night, and holiday premium rates moved to attendance on 2026-01-01 — the payroll page is explicitly the old, superseded rule. Attendance's `sec-hard-overtime` table is flagged as "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," which matches today's date (2026-09-20), so no need to consult the superseded `hard-overtime-v2` or `overtime-rate-table` versions. The table listed 64 day/hours/place row combinations plus separate legend files for decoding day/hours/place codes into the D/H/P codes — but the question already gave the codes directly (D4, H1, P4), so the row address could be built by pattern-matching the naming convention without needing to open the legends. That pattern-matching is the one place this walk could go wrong if the address weren't exactly as printed in the table listing, but I copied `hard-overtime-row-day-d4-hours-h1-place-p4` verbatim from the table output rather than constructing it by hand.
