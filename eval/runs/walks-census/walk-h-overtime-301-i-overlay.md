1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, about ninety minutes, out at a client's office: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and pay calc rules likely here" --member /v1/regions/attendance "time/overtime rounding rules likely here"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_de67de --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body

2. **Answer**: Multiplier 2.67x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body

4. **Notes**: The overtime rate subject has three versions gated by date, and the legend-revision page warns the oldest version says nothing about being superseded — checking it first was necessary to avoid grabbing `overtime-rate-table` (the oldest) by reflex. With today's date (2026-09-21) falling after 2026-01-01, the current table `sec-hard-overtime` applied, so I never needed to go near `hard-overtime-v2`, but that would not have been true for a 2025-dated question. The three qualifiers (day/hours/place) are each resolved through a dedicated legend rather than guessed: "two in the morning" maps to day code D4 (not a weekday/weekend/holiday distinction as I first assumed — the legend's own example row for that exact phrase is what settled it), "about ninety minutes" maps to hours code H1, and "out at a client's office" maps to place code P2, all matched by exact or near-phrase in the legend tables rather than inference. The overlay's `close` reported all five addresses I used as "reached... from somewhere the overlay never named" — I had only added the two region-level members (`payroll`, `attendance`) to the overlay and never formally added the specific file/legend addresses as members before reading them, which is a minor procedural slip but did not affect the answer since the addresses came from the correct working set regardless.
