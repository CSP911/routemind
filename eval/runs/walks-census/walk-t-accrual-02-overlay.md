1. Commands
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In September 2023, how much leave was accrued/granted for two years continuous service, under the version in force on that date?" --member /v1/regions/attendance "leave accrual rules by service length live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py overlay add --id ov_2026-09-20_3c0933 --address /v1/nodes/leave-accrual --why "oldest version, in force until 2024-07-01, covers Sept 2023"
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py table /v1/nodes/sec-entitlement-cases
./bench/rmcli.py overlay close --id ov_2026-09-20_3c0933 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/leave-accrual /v1/nodes/accrual-rule/body

2. Answer
15 days. Under the version in force in September 2023 (the oldest of the three leave-accrual versions, in force until 2024-07-01), someone with 1 year and over of service — which covers two years — is granted 15 days per fiscal year. The next step up (an extra day every 2 years, capped at 25) only starts at 3 years of service, so two years still falls in the flat 15-day bracket.

3. Source
/v1/nodes/hard-accrual-legend-revision/body (establishes which version applies to a September 2023 date)
/v1/nodes/accrual-rule/body (the entitlement table itself: "1 year and over → 15 days")

4. Notes
The leave accrual subject has three versions in force at different date ranges (until 2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that the oldest version does not say anything about being superseded — so reading /v1/nodes/leave-accrual alone would look complete and current even though it isn't, for a 2023 date. The correct old-version address (/v1/nodes/leave-accrual) is not listed as a member of /v1/regions/attendance directly in the overlay table printed at hop 1; it only surfaced by opening /v1/nodes/annual-leave, which is a genuine table-of-tables step, not a shortcut. Two years of service sits inside the "1 year and over" bracket, not the "3 years and over" bracket, so it was worth double-checking that two years isn't treated as a special edge case — I opened /v1/nodes/sec-entitlement-cases to confirm, but that section only covers transfers/rehires/proration, not plain continuous service, so it doesn't apply here.
