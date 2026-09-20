1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py read /v1/nodes/annual-leave/body

2. **Answer**
You accrue 0.94 days per month, and the carry-over limit — the most you can still be holding when the year turns over into January — is 13 days. (Notice required to take leave under this row is 3 working days; leave does not accrue during unpaid leave.)

3. **Source**
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body

4. **Notes**
The attendance table lists two separate leave-entitlement systems that look interchangeable at a glance: the general `/v1/nodes/annual-leave` page (flat entitlement by service length, days "granted on 1 January" and explicitly "do not roll over") and the current `/v1/nodes/sec-hard-accrual` table (64 rows indexed by type/tenure/site code, in force since 2026-01-01, each row with its own "carry-over limit"). These directly contradict each other on rollover if you mix them up. Since the question gives explicit type/tenure/site codes (E2/T3/L4), it clearly targets the hard-accrual table, not the general annual-leave page — I read the annual-leave page only to confirm it was the wrong system, not to source the answer from it. Also worth flagging: `hard-accrual-legend-revision` warns the accrual rules have three superseded versions; I used the one explicitly marked current and in force from 2026-01-01, which covers today's date (2026-09-20), so no version confusion applies here — but it's an easy trap for anyone not checking the effective dates.
