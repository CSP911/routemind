1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A saturday, about ninety minutes, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/standby rules likely live with attendance" --member /v1/regions/payroll "overtime pay multiplier likely defined in payroll"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_cb23f5 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body

2. **Answer**: Multiplier 1.74x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body

4. **Notes**: The overtime rate table has three superseded versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and current from 2026-01-01), and the legend-revision doc warns explicitly that the oldest version says nothing about being replaced — so grabbing the first hit without checking the revision doc would have silently returned a stale rate. Since today is 2026-09-20/21, the current table `sec-hard-overtime` applied, but this is exactly the kind of question where a 2025-dated version of the same question would need the middle table instead. The three legends (day/hours/place) mapped cleanly and exactly onto the question's wording ("a Saturday" → D2, "about ninety minutes" → H1, "on standby at home" → P3 — all literal matches, no nearest-neighbor guessing needed), so the row lookup itself was unambiguous once the legends were read. I initially added the payroll region to the working set on the assumption overtime multipliers might be defined there, but `hard-moved-overtime` in payroll confirmed overtime premiums were moved to attendance on 2026-01-01, so the attendance-side table was correct and payroll contributed nothing to the final answer.
