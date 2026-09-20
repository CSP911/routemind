1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body

2. **Answer**
Accrues 0.82 days per month. Carry-over limit (max you can still be holding going into January) is 8 days.
This is from the current accrual table, in force since 2026-01-01, for type E2 (two-year contract), tenure T2 (been here two years), site L2 (Busan branch).

3. **Source**
- /v1/nodes/hard-accrual-legend-type/body
- /v1/nodes/hard-accrual-legend-tenure/body
- /v1/nodes/hard-accrual-legend-site/body
- /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body

4. **Notes**
The three qualifiers in the question (contract type, tenure, site) each had to be translated through a separate legend into a code (E2/T2/L2) before the actual row could be addressed — the row addresses aren't guessable from plain language, they're only reachable via the three legend files. Easy to miss one of the three legends and grab a row with a partial match. Also worth flagging: the table's own listing warned of three historical versions of the accrual rules (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual`); today's date (2026-09-20) falls in the current version's effective range (from 2026-01-01), so the older two were correctly not consulted, but it would be easy to grab a superseded row by mistake if the "in force" note weren't checked.
