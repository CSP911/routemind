1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body

2. **Answer**: Multiplier 1.65x. Minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body

4. **Notes**: The payroll region's overtime page (`/v1/nodes/hard-moved-overtime/body`) warns that overtime premiums moved to attendance on 2026-01-01, so I skipped it and went straight to attendance — worth flagging because a naive search would land in payroll first and dead-end there. Within attendance, there were explicitly superseded overtime tables (`hard-overtime-v2`, and an older `overtime-rate-table` referenced but not listed) alongside the current one (`sec-hard-overtime`, in force since 2026-01-01); today's date (2026-09-20) falls inside the current table's validity window, so I used that one and did not need to consult the superseded versions. The three legends (day/hours/place) had to be resolved independently before the row address could be built: "an ordinary Tuesday" → D1, "eleven hours" → H4, "from home" → P4 (distinct from "on standby at home" = P3, which was the one place I nearly picked wrong — the two labels are easy to conflate but the legend lists them as separate codes). No ambiguity in the final row lookup once the three codes were fixed.
