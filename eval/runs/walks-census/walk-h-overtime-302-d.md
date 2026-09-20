1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body

2. **Answer**: Multiplier is 2.70x; minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body

4. **Notes**: The payroll region's table explicitly warns that overtime premiums moved to attendance on 2026-01-01, so the payroll table itself is a dead end for this question — good thing it flagged the redirect instead of silently offering a stale answer. Within attendance, there are two competing tables: the current one (`sec-hard-overtime`, in force since 2026-01-01) and an older superseded one (`hard-overtime-v2`, 2024-07-01 to 2025-12-31), plus a legend-revision file explaining there are three versions total. Since today's date is 2026-09-20, the current table was clearly the right pick, but it would be easy to grab the wrong version if you weren't paying attention to the "superseded" labeling. Once inside `sec-hard-overtime`, the row address for D4/H1/P3 was printed verbatim in the table listing, so no guessing or construction was needed — just picked the matching row directly.
