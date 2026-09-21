1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T3, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carryover cap by employee type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_eb70cc --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body

2. **Answer**:
- Accrues 0.60 days per month.
- Carry-over limit: 12 days — this is the cap on what can still be held (e.g. into January, at year-end rollover).
(Figures from the current accrual table, in force since 2026-01-01, which applies to today's date of 2026-09-20/21.)

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body — confirmed which of the three accrual table versions applies to a question asked today
- /v1/nodes/sec-hard-accrual — the current accrual table, used to locate the E1/T3/L3 row
- /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body — the row with the actual figures (0.60 days/month accrual, 12-day carry-over limit)

4. **Notes**:
There are three separate versions of the leave accrual document (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest one is wrong for any date before 2026-01-01. Today's date (2026-09-20) falls inside the newest version's range, so `sec-hard-accrual` was correct here, but this is exactly the kind of question where grabbing the first accrual-looking table without checking the revision legend would give a stale answer for a question dated a year earlier. The "how much can I still be holding in January" phrasing doesn't map to an obvious field name — the table only exposes a "Carry-over limit, days" figure, which I'm reading as the answer to that question (the cap on balance you can still be holding into the new year), but the table itself never uses the word "January," so this connection is inferred rather than stated outright.
