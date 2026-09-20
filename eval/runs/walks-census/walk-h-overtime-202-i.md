1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body

2. **Answer**: Multiplier 2.22x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body

4. **Notes**: The payroll area's overtime table is explicitly stale — a warning on /v1/regions/payroll says overtime premiums moved to attendance on 2026-01-01, so the real answer lives in /v1/nodes/sec-hard-overtime, not in payroll's own /v1/nodes/hard-moved-overtime. Easy to go wrong here by reading the payroll overtime page and stopping. Within attendance, there were also two superseded overtime versions (hard-overtime-v2, overtime-rate-table) sitting right next to the current one (sec-hard-overtime); had to check the "in force from 2026-01-01" language to be sure I was on the current table rather than the 2024-07-01–2025-12-31 version. The three qualifiers (day/hours/place) each had to be translated through a separate legend file before the row address could be built — "Liberation Day" → D3, "about ninety minutes" → H1 (an exact wording match in the legend), "on standby at home" → P3 (distinct from plain "from home" = P4, which was a plausible mix-up). No ambiguity once the legends were read carefully.
