1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "An ordinary tuesday, about ninety minutes, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "standby time and overtime multipliers are likely tracked under attendance/working hours rules"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_199aeb --outcome answered --used /v1/regions/attendance /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body

2. **Answer**: Multiplier 1.26x, minutes rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body

4. **Notes**: The overtime table has three superseded versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 — today (2026-09-20/21) falls after that cutoff, so the current table `sec-hard-overtime` was correct, but it would have been easy to skip that check and just grab whichever table looked newest. The three qualifiers (day/hours/place) each needed their own legend lookup before the row address could be built: "an ordinary tuesday" → D1, "about ninety minutes" → H1 (matched the legend's example phrasing almost verbatim), and "on standby at home" → P3 — this last one was the one place I nearly slipped, since "from home" (P4) is a separate, distinct category from "on standby at home" (P3) in the legend, and conflating the two would have given the wrong row.
