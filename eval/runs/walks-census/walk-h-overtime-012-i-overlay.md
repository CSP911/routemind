1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "An ordinary tuesday, three hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and rounding rules likely live in payroll" --member /v1/regions/attendance "standby/on-call time tracking might be defined in attendance"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7bda2d --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body

2. **Answer**: Multiplier 1.38x; minutes rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body

4. **Notes**: The overtime rate subject has three versions (`overtime-rate-table` until 2024-07-01, `hard-overtime-v2` for 2024-07-01–2025-12-31, `sec-hard-overtime` from 2026-01-01 onward), and the legend-revision page warns the oldest version says nothing about being replaced — reaching for the newest without checking the date would have been wrong for a 2025 question, and reaching for the oldest would be wrong for today. Today's date (2026-09-20) falls squarely in the current table's period, so `sec-hard-overtime` was correct, but this is exactly the kind of question the warning exists for. The row table is indexed by three separate legend-driven codes (day/hours/place) rather than natural language, so all three legends had to be read before the row address could be built: "an ordinary Tuesday" → D1, "three hours" → H2 (matches the legend's own listed value exactly, no nearest-neighbor guess needed), "on standby at home" → P3 (distinct from plain "from home" = P4, which was the one place a careless reading could have picked wrong). No ambiguity once the legends were read; the only risk was skipping the revision-date check or conflating P3/P4.
