1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body

2. **Answer**: Multiplier is 2.43x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body

4. **Notes**: The payroll region's overtime page is a trap — it explicitly warns that overtime premiums moved to attendance on 2026-01-01, so the answer had to come from `/v1/regions/attendance`, not payroll. Within attendance there were also superseded overtime tables (`hard-overtime-v2` and legend-revision warnings) sitting alongside the current one; had to be careful to pick `sec-hard-overtime`, the table explicitly marked as in force from 2026-01-01 (today is 2026-09-20, so it applies). The row itself isn't looked up directly by plain-English terms — it requires decoding "Liberation Day" → D3, "six hours" → H3, and "out at a client's office" → P2 via three separate legend documents before the actual row address (`hard-overtime-row-day-d3-hours-h3-place-p2`) can be constructed from the pattern shown in the table listing. No ambiguity in the final mapping — all three qualifiers matched a legend row exactly, no nearest-entry fallback was needed.
