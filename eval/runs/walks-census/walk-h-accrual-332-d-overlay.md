1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T4, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual and carryover/balance cap rules likely live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_86fd79 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body

2. **Answer**:
For type E4, tenure T4, site L3: accrues 1.64 days per month. Carry-over limit is 15 days — that is the maximum that can still be held (e.g. into January).

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body

4. **Notes**:
The tricky part here is that leave accrual has three versions in force over different date ranges, and reaching for the newest table by reflex is explicitly called out as wrong for questions dated before 2026-01-01. The legend-revision doc made clear today's date (2026-09-20) falls under the current table `sec-hard-accrual` (in force 2026-01-01 onward), so no ambiguity in this case — but it's easy to see how skipping that check could silently apply the wrong version's numbers on a question dated earlier. The phrase "how much can I still be holding in January" isn't a separate figure from a "carryover" concept elsewhere — it maps directly onto the row's "Carry-over limit, days" field, which is the cap on balance held into the new year.
