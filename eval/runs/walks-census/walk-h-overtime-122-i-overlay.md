1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, six hours, standby at home: what multiplier applies, and what rounding for minutes?" --member /v1/regions/payroll "standby/overtime pay multiplier and minute rounding is a payroll topic"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay add --id ov_2026-09-21_59d542 --address /v1/regions/attendance --why "hard-moved-overtime redirect: overtime/standby premiums live in attendance's sec-hard-overtime since 2026-01-01, question date 2026-09-20 is after that"
./bench/rmcli.py overlay remove --id ov_2026-09-21_59d542 --address /v1/regions/payroll --why "redirect confirms overtime/standby now lives in attendance sec-hard-overtime, not payroll, for dates on/after 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_59d542 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body

2. **Answer**: Multiplier 1.98x. Minutes rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-moved-overtime/body
- /v1/nodes/hard-overtime-legend-revision/body
- /v1/nodes/hard-overtime-legend-day/body
- /v1/nodes/hard-overtime-legend-hours/body
- /v1/nodes/hard-overtime-legend-place/body
- /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body

4. **Notes**: The obvious first guess — payroll — is wrong for this question's date. Payroll still has the old overtime page (`payslip-overtime`), and nothing on it says it was replaced, so it would look correct if read in isolation. The `hard-moved-overtime` redirect is the only thing that says overtime moved to attendance's `sec-hard-overtime` on 2026-01-01, and the question date (2026-09-20) falls after that cutover, so payroll had to be dropped from the working set. Even inside attendance there's a second trap: `sec-hard-overtime` is itself the third of three versioned tables (pre-2024-07-01, 2024-07-01–2025-12-31 as `hard-overtime-v2`, and current from 2026-01-01), and the legend-revision page warns explicitly that grabbing the newest table without checking the date is wrong for older questions — it happened to be right here only because the date checked out. Mapping the three qualifiers also required care: "on standby at home" is place P3, distinct from "from home" (P4) — the two read similarly and it would be easy to pick the wrong one without reading the place legend closely.
