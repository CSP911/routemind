1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, six hours, at a client's office: what overtime multiplier applies, and to what rounding are minutes taken?" --member /v1/regions/attendance "overtime rules, weekend work often covered under attendance" --member /v1/regions/payroll "overtime pay multiplier and rounding likely defined in payroll"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_eefa5a --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body

2. **Answer**: Multiplier is 1.95x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
- /v1/nodes/hard-overtime-legend-hours/body (six hours → hours H3)
- /v1/nodes/hard-overtime-legend-place/body (out at a client's office → place P2)
- /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body (the figures: multiplier 1.95x, rounding to nearest 15 minutes)

4. **Notes**: The overlay members I picked (attendance and payroll regions) both turned out to be red herrings for the direct answer — the payroll region even has a warning node (`hard-moved-overtime`) saying overtime premiums moved out of payroll into attendance as of 2026-01-01, which confirmed I was right to lean on attendance rather than payroll. The real trap was version drift: the attendance table listed both `sec-hard-overtime` (current, in force from 2026-01-01) and `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31), plus a `hard-overtime-legend-revision` warning node flagging three different versions with different figures. Since today (2026-09-20/21) falls after 2026-01-01, I used the current table only and did not touch the superseded ones — but it would have been easy to grab the wrong version's row by not checking the effective dates first. The row lookup itself was mechanical once the three legends (day/hours/place) were read — "a Saturday" maps directly to D2, "six hours" to H3 exactly (no nearest-match needed), and "out at a client's office" to P2 exactly, so no ambiguity there.
