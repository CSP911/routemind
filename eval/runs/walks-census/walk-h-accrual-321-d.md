1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body

2. **Answer**
For type E4, tenure T3, site L2 (current table, in force from 2026-01-01):
- Accrues 1.54 days of leave per month.
- Carry-over limit into the new year (i.e. how much can still be held in January): 11 days.

3. **Source**
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body

4. **Notes**
The row for E4/T3/L2 was addressable directly from the /v1/nodes/sec-hard-accrual table listing — no need to consult the type/tenure/site legends since the question already gave codes rather than plain-language descriptions. The one place this could have gone wrong: the attendance area's table listing carries a loud warning that leave accrual has three versions (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual`), each covering different date ranges. It would have been easy to grab a superseded version by accident. I confirmed via the row's own footer that this is the version in force from 2026-01-01, which covers today's date (2026-09-20), so it's the correct one to use. I read "how much can I still be holding in January" as asking about the carry-over limit (the balance allowed to roll into the new year) rather than a projected balance calculation — the table only states the flat carry-over limit, not a month-by-month accrual schedule, so that's the only figure available to answer that part.
