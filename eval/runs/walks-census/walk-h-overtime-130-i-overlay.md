1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A saturday, eleven hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier likely defined in payroll rules" --member /v1/regions/attendance "attendance may define how overtime hours are logged/rounded"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_80f67e --address /v1/regions/payroll --why "overtime premiums moved to attendance on 2026-01-01, per hard-moved-overtime warning; payroll no longer authoritative"
./bench/rmcli.py overlay close --id ov_2026-09-21_80f67e --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body

2. **Answer**: Multiplier 2.04x. Minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p1/body

4. **Notes**: The overlay creation itself was the near-miss: I first put payroll in the working set because "multiplier" sounds like a pay rule, but a warning file (`hard-moved-overtime`) surfaced right in that region's table saying overtime premiums moved out of payroll to attendance as of 2026-01-01 — so I removed payroll from the overlay before closing rather than reading further into it. The bigger trap was version drift: overtime rate has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and the legend-revision file explicitly warns that "the oldest says nothing at all about having been replaced," so grabbing the first table found without checking `hard-overtime-legend-revision` would silently give a stale rate. Today (2026-09-21) falls in the current version, so `sec-hard-overtime` was correct. The three qualifiers (day/hours/place) also aren't self-evident from the question's plain words — they only resolve to D2/H4/P1 via the three separate legend files, each of which says it is "the only place the mapping is written down," so skipping any one of them would have made the final row address unguessable. Finally, the close command reported the used addresses as "reached" rather than matched overlay members — that's just because I'd only added region-level members, not the specific leaf files, to the overlay; it didn't indicate an error in the answer.
