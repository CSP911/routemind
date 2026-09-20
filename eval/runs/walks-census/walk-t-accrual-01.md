1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py read /v1/nodes/leave-accrual/body

2. **Answer**: 15 days, granted whole on 1 January, under the bracket "1 year and over" (two years of continuous service does not reach the "3 years and over" bracket, which is 15 + 1 per 2 further years).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (establishes which version covers March 2023)
- /v1/nodes/accrual-rule/body (the entitlement table)
- /v1/nodes/leave-accrual/body (confirms the "one year and over" bracket = fifteen days, granted whole on 1 January)

4. **Notes**: The /v1/regions/attendance table listing is a trap for this question — it surfaces `hard-accrual-v2` (in force 2024-07-01 to 2025-12-31) and `sec-hard-accrual` (current, since 2026-01-01) directly, but does NOT list the oldest version at all. Grabbing either of those without checking dates would have given the wrong-era answer for a March 2023 question. The legend-revision file explicitly warns "reaching for the newest is wrong for anything before 2026-01-01" and gives the oldest version's short name as `leave-accrual`, but not its full address — that had to be found by backtracking to /v1/nodes/annual-leave → /v1/nodes/leave-accrual, which isn't linked from the attendance table's visible list either. Two separate documents live at that node (leave-accrual/body and accrual-rule/body); both were read since the table row descriptions didn't make clear which one held the actual day-count table versus the narrative explanation — they turned out to be complementary and consistent, not conflicting.
