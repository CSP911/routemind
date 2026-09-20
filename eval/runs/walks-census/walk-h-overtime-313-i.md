1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body

2. **Answer**: Multiplier 2.85x, rounded to the nearest 10 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body
- /v1/nodes/hard-overtime-legend-hours/body
- /v1/nodes/hard-overtime-legend-place/body
- /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body

4. **Notes**: The payroll region's overtime page is a dead end by design — it explicitly warns overtime premiums moved to attendance on 2026-01-01, so the walk had to redirect there. The real trap is the day legend: "two in the morning" is listed directly as day D4 in the legend table (not "an ordinary Tuesday" or any date-based lookup) — it would be easy to assume day type needs to be derived from today's date (2026-09-20) and go hunting for what day of the week that is, or to treat "two in the morning" as purely a time-of-day/hours signal rather than realizing it independently selects the day axis. The legend explicitly says "two in the morning" maps to day D4, so no date arithmetic was needed at all — the three qualifiers (day, hours, place) each came from a literal phrase match in their respective legend, not from any computation.
