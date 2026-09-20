1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body

2. **Answer**: Multiplier 1.62x; minutes rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body

4. **Notes**: The payroll region's overtime page is a dead end by design — it explicitly says overtime premiums moved to attendance on 2026-01-01, so following the payroll table further would have wasted the walk. Within attendance, there's a legend-revision warning stating the overtime rate has three versions (until 2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward); today's date (2026-09-20) falls in the current version (`sec-hard-overtime`), so the older `hard-overtime-v2` table had to be deliberately skipped rather than assumed correct. The row table itself is not indexed by plain-English terms — it required reading three separate legend files (day/hours/place) to translate "an ordinary Tuesday" → D1, "eleven hours" → H4, and "on standby at home" → P3 before the right of 64 rows could be addressed. No ambiguity in the mapping itself; the main risk was picking a stale version or drilling into the wrong (payroll) region first.
