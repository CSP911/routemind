1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body

2. **Answer**: For type E2, tenure T2, site L2: accrues 0.82 days per month; the carry-over limit is 8 days, so up to 8 days can still be held into January. (This row does not accrue during unpaid leave, and any approved excess above these figures is decided case-by-case by the budget holder.)

3. **Source**: /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body

4. **Notes**: The attendance area warns that leave accrual has three versions in force over different date ranges (`leave-accrual` until 2024-07-01, `hard-accrual-v2` from 2024-07-01 to 2025-12-31, and `sec-hard-accrual` from 2026-01-01 onward), and explicitly says reaching for the newest is wrong for dates before 2026-01-01. Today is 2026-09-20, so the current table (`sec-hard-accrual`) was the correct one to use — but this was worth checking rather than assuming, since the trap is clearly built for questions dated in 2025. The E2/T2/L2 row existed directly under the current table's 64-row index, so no need to consult the site/tenure/type legends to decode the codes — the question already gave qualifiers in the table's own coding scheme. The "how much can I still be holding in January" phrasing maps to the row's "Carry-over limit" field, which wasn't obviously named that way going in — it took reading the actual row body to confirm the carry-over limit is what answers a balance-at-year-turn question, rather than, say, the annual entitlement or a cap defined elsewhere.
