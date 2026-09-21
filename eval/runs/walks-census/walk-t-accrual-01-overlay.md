1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In March 2023, how much leave was accrued or granted for someone with two years of continuous service, under the version of leave accrual in force at that date?" --member /v1/regions/attendance "leave accrual by years of service is likely defined here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py overlay add --id ov_2026-09-20_dfa589 --address /v1/nodes/leave-accrual --why "the oldest leave accrual version, in force until 2024-07-01, per hard-accrual-legend-revision — covers March 2023"
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py table /v1/nodes/sec-entitlement-cases
./bench/rmcli.py overlay close --id ov_2026-09-20_dfa589 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/leave-accrual /v1/nodes/accrual-rule/body

2. **Answer**: 15 days. (March 2023 falls under the oldest version of leave accrual, which was in force until 2024-07-01. Under that version's standard table, "1 year and over" of service grants 15 days, and the next step up only applies "3 years and over." At exactly two years of continuous service, the applicable bracket is "1 year and over" → 15 days.)

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (established which version covers March 2023)
/v1/nodes/leave-accrual (confirmed this node is the entitlement table for that version)
/v1/nodes/accrual-rule/body (the actual table with the days-by-service figures)

4. **Notes**: The overlay's first pass over /v1/regions/attendance did not surface an address literally named "leave-accrual" — it only listed /v1/nodes/annual-leave, which turned out to be a parent node whose own sub-table (/v1/nodes/leave-accrual) held the actual entitlement data. Easy to miss if you don't open annual-leave as a table itself. Also worth flagging: this domain has three superseded/current versions of leave accrual (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and the legend page explicitly warns that "the oldest says nothing at all about having been replaced" — so without checking the legend first, it would have been easy to read /v1/nodes/leave-accrual, find no revision warning on it, and mistake it for the current rule rather than the one to use only for March 2023. I also checked /v1/nodes/sec-entitlement-cases to make sure "two years, continuous service" wasn't a listed special case (transfers/rehires/proration) — it wasn't, so the standard table applies directly.
