1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body

2. **Answer**
Multiplier: 1.50x. Rounding: to the nearest 15 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body

4. **Notes**
The payroll region's overtime page (/v1/nodes/hard-moved-overtime/body, not opened directly but flagged in the payroll table listing) warns that overtime premiums moved to attendance on 2026-01-01, so the first table I opened (payroll) was a dead end by design — a trap for anyone who assumes "overtime pay" belongs with payslip lines. Within attendance, there are three overtime tables (a "v2" for 2024-07-01–2025-12-31, an older superseded one, and `sec-hard-overtime` as current since 2026-01-01); today's date (2026-09-20) falls inside the current table's range, so `sec-hard-overtime` was the correct pick and I didn't need to touch the superseded ones. The row-selection step is the part most likely to trip someone up: the three legends (day, hours, place) must each be read and mapped independently before the row address can be assembled — "an ordinary Tuesday" → D1, "six hours" → H3, "on standby at home" → P3 — and the row filenames are addresses printed by the table, not something to hand-construct from guesswork, so I only used the exact address the table listed (hard-overtime-row-day-d1-hours-h3-place-p3). No ambiguity in the mapping itself; all three inputs matched a legend row exactly, no nearest-entry substitution needed.
