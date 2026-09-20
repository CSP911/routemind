1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body

2. **Answer**: Multiplier is 1.71x. Minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body

4. **Notes**: The payroll region's table warned up front that overtime premium rates moved to attendance on 2026-01-01 — the payroll page itself (`hard-moved-overtime`) is the old, superseded rule, so I didn't read it and went straight to attendance instead. Within attendance there were two overtime tables listed: `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31) and `sec-hard-overtime` (current, in force from 2026-01-01). Since today's date is 2026-09-20, the current table is the right one, confirmed again by the "In force from 2026-01-01" line inside the row itself. The D2/H1/P2 row was addressable directly by name once the table listing appeared, so no legend lookups were needed to resolve the codes — the question already gave day/hours/place as codes matching the table's own naming scheme.
