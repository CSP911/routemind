1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A saturday, eleven hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and pay-related rounding rules are typically in payroll" --member /v1/regions/attendance "attendance rules may cover work-from-home and time tracking/rounding"
./bench/rmcli.py overlay add --id ov_2026-09-21_084d69 --address /v1/nodes/sec-hard-overtime --why "current overtime rate table, in force from 2026-01-01, by day/hours/place - matches Saturday/11h/home"
./bench/rmcli.py overlay add --id ov_2026-09-21_084d69 --address /v1/nodes/hard-overtime-legend-revision/body --why "warns overtime rate has 3 versions with different dates — need to confirm which applies to today 2026-09-21"
./bench/rmcli.py overlay remove --id ov_2026-09-21_084d69 --address /v1/nodes/hard-moved-overtime/body --why "confirms overtime premiums live in attendance, not payroll, since 2026-01-01 — already established, not needed further"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_084d69 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body

2. **Answer**: Multiplier 2.13x, rounding to the nearest 20 minutes. (Saturday → day D2, eleven hours → hours H4, from home → place P4, current table in force since 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body
- /v1/nodes/hard-overtime-legend-hours/body
- /v1/nodes/hard-overtime-legend-place/body
- /v1/nodes/hard-overtime-legend-revision/body
- /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body

4. **Notes**: The overtime area first appears under attendance, not payroll — a `hard-moved-overtime` note in the payroll region explicitly warns that overtime premiums moved to attendance on 2026-01-01, so starting the search in payroll (a reasonable first guess since it's a pay multiplier) would be a dead end without that pointer. The place legend was the sharpest trap: "from home" (P4) and "on standby at home" (P3) are both listed and both plausible glosses for a vague real-world phrase, but the question used the exact wording "from home," so P4 was the direct match rather than an inference. Also had to actively check the legend-revision doc rather than assume the newest table applies — it explicitly says a 2025-dated question would need the superseded `hard-overtime-v2` table instead. Since today's date is 2026-09-21, the current table (`sec-hard-overtime`) was correct, but the check was necessary rather than a formality. One overlay command batch (three chained commands) hit the tool's 120s timeout and got backgrounded; a background notification reported exit code 1 for the batch, but on inspection the individual `add` had actually already succeeded (a retry returned HTTP 409 "already in this overlay"), so no real error occurred — just a chaining/timeout artifact.
