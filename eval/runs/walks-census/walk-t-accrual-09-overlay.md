1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For something dated 29 June 2024 (two days before the first change), how much leave was accrued/granted for someone with two years of continuous service? Use the version in force on that day." --member /v1/regions/attendance "leave accrual by tenure is an attendance policy topic"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py overlay close --id ov_2026-09-20_78deca --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/annual-leave /v1/nodes/leave-accrual /v1/nodes/accrual-rule/body

2. **Answer**: 15 days. (Under the oldest/original leave-entitlement version, in force until 2024-07-01, someone with "1 year and over" of service — which covers 2 years, since the next tier only starts at 3 years — is granted 15 days.)

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/annual-leave
/v1/nodes/leave-accrual
/v1/nodes/accrual-rule/body

4. **Notes**: The overlay's leave-accrual member list surfaced `hard-accrual-v2` (in force 2024-07-01 to 2025-12-31) prominently, and it would have been easy to grab that one on a reflex "2024 → v2" match. But the legend page (`hard-accrual-legend-revision/body`) makes clear the "first change" mentioned in the question is the 2024-07-01 cutover, and the question's date — 29 June 2024 — sits two days *before* that cutover, so it's still governed by the oldest, pre-2024-07-01 version at `leave-accrual`/`accrual-rule`. That oldest version's document "says nothing at all about having been replaced," per the legend, so reading it in isolation gives no clue a newer version exists — the legend page is the only place that establishes the date boundary. The table for that version is banded by "Under 1 year / 1 year and over / 3 years and over," not by exact year counts, so two years of service has to be mapped to the "1 year and over" row (15 days) rather than assuming a per-year increment applies before year 3.
