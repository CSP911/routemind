1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py read /v1/nodes/leave-accrual/body

2. **Answer**
15 days, granted whole on 1 January. (January 2024 falls under the oldest accrual rule, in force until 2024-07-01: "1 year and over" = 15 days; the next step up, "3 years and over," does not apply to someone with only two years of service.)

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (established which version applies to the date)
/v1/nodes/accrual-rule/body (the table: 1 year and over → 15 days)
/v1/nodes/leave-accrual/body (confirms 15 days granted whole on 1 January, and that the 3-years-and-over step is a further increase, not the applicable band)

4. **Notes**
The attendance region's table listing (`/v1/regions/attendance`) only shows two of the three accrual versions directly — `hard-accrual-v2` (2024-07-01 to 2025-12-31) and `sec-hard-accrual` (current, since 2026-01-01). The oldest version, which is the one that actually answers a January 2024 question, is not listed there at all; it had to be found by reading the legend-revision warning page, which named its index as `leave-accrual` but gave no address. That address only turned up by going back to `/v1/nodes/annual-leave`, a node not reachable from the accrual legend page itself. Anyone who took the attendance table's listing at face value and picked the "supersedes" version starting 2024-07-01 (hard-accrual-v2) would have answered with the wrong regime for a January 2024 date — the legend page was explicit that this is the mistake to avoid. Also worth flagging: the table on `/v1/nodes/accrual-rule/body` lists "1 year and over" and "3 years and over" as if separate rows, but `/v1/nodes/leave-accrual/body` clarifies the second is additive to the first, not a replacement — for two years of service only the first row (15 days) applies, so this didn't end up mattering here, but it's an easy misread for other tenures.
