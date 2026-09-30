1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, three hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "night-time standby overtime multiplier likely a payroll/overtime pay rule" --member /v1/regions/attendance "on-call/standby at home may be tracked as an attendance category with its own rounding rule"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_87e08d --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body

2. **Answer**: Multiplier 2.82x. Minutes are rounded to the nearest 10 minutes.

3. **Source**:
- /v1/nodes/hard-moved-overtime/body (confirms overtime premiums live in attendance, not payroll, from 2026-01-01)
- /v1/nodes/hard-overtime-legend-revision/body (confirms the current table, not an older version, covers today's date)
- /v1/nodes/hard-overtime-legend-day/body (maps "two in the morning" → day D4)
- /v1/nodes/hard-overtime-legend-hours/body (maps "three hours" → hours H2)
- /v1/nodes/hard-overtime-legend-place/body (maps "on standby at home" → place P3)
- /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body (the row itself: 2.82x, rounded to the nearest 10 minutes)

4. **Notes**: The main trap here was starting in payroll — the question smells like a pay-rate question, and payroll even has a `payslip-overtime` overtime line, but `hard-moved-overtime/body` warns that this was superseded on 2026-01-01 and the real rule now lives in attendance's `sec-hard-overtime`. A second trap was the three-version history of that table (`hard-overtime-legend-revision`): today's date (2026-09-21) falls in the current version's range, but a question dated in 2025 would need the superseded `hard-overtime-v2` instead — this is exactly the "neither extreme" case the legend calls out. Once in the current table, the qualifiers were not literal — "two in the morning" maps to day-type D4 (not a weekday/weekend distinction as I first assumed), "three hours" maps to duration band H2, and "on standby at home" is distinct from plain "from home" (P3 vs P4) — easy to conflate if read quickly. Picking the wrong place code (P4 instead of P3) would have been the most likely mistake.
