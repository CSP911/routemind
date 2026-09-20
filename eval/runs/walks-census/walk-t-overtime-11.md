1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
```

2. **Answer**
- 2023 (rule in force until 2024-07-01): ordinary overtime beyond the 40-hour week paid **+50% (1.5x)**, a single flat rate.
- By 2025 (rule in force 2024-07-01 to 2025-12-31): the flat "ordinary overtime" category was replaced by a day × hours grid. The multiplier ranges from **1.20x** (day 1, hour 1 of overtime — the lowest/base cell) up to **1.65x** (day 4, hour 4 — the highest cell), rising in 0.03x steps per hour and 0.12x per day. There is no single flat "2025 rate" comparable to the 2023 one — it depends on which day of the week and which hour of overtime is being paid.

3. **Source**
- /v1/nodes/hard-overtime-legend-revision/body (routing: which version covers which date)
- /v1/nodes/overtime-rate-table/body (2023 rate, until 2024-07-01)
- /v1/nodes/hard-overtime-v2/body (2025 rate, 2024-07-01 to 2025-12-31)

4. **Notes**
- Payroll's own page (`payslip-overtime`) also states a flat +50% overtime rate with no date qualifier, and looks like a complete answer on its own — it would have been easy to stop there. But `hard-moved-overtime` warns that payroll's overtime page is only correct pre-2026 and points to attendance for anything current, and attendance in turn has its own three-version legend (`hard-overtime-legend-revision`) showing the rate changed again *within* the pre-2026 period, on 2024-07-01. Payroll's page never mentions that mid-period change at all — it's silent about being superseded, exactly as the legend page warns ("the oldest says nothing at all about having been replaced"). Trusting the payroll page alone would have given the 2023 figure for both years and silently missed the 2024-07-01 change.
- The real trap for 2025: the legend explicitly says a 2025 question is answered by the *middle* version (`hard-overtime-v2`), not the oldest and not the current (2026+) table — "the one where taking either extreme is wrong." It would be easy to jump straight to `sec-hard-overtime` (the current, most detailed, three-qualifier table) since it looks most authoritative, and get a 2026+ figure instead.
- The 2025 version itself is confusing on its own terms: it replaces the old category system (ordinary overtime / night / holiday) with a day×hours grid, and never labels any cell as "ordinary overtime beyond the 40-hour week" the way the 2023 table did. Its closing sentence — "the multiplier ... followed the overtime rates rule unchanged until 2026-01-01" — reads as if the multiplier didn't change, directly contradicting the grid of different values sitting above it. I read this as sloppy/leftover phrasing referring to non-multiplier mechanics (rounding, approval), not the multiplier itself, since the grid is unambiguous, but flagging it because it could mislead a careless read into reporting "still 1.5x, unchanged" for 2025.
