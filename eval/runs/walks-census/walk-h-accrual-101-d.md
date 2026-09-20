1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body

2. **Answer**
For type E2, tenure T1, site L2 (current table, in force from 2026-01-01): accrues 0.74 days per month. The carry-over limit is 5 days — that is the most that can still be held into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed the current table applies to today's date, 2026-09-20)
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body (the figures)

4. **Notes**
There are three versions of the accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 — the old page doesn't announce that it's been superseded. Since today is 2026-09-20, the current table (`sec-hard-accrual`) is correct, but this is an easy place to go wrong if the date isn't checked first. The question's phrasing "how much can I still be holding in January" isn't a direct field name — I read it as asking for the carry-over limit (5 days), since that's the cap on what remains held into the new year. The row also lists a "notice required" figure and "accrues during unpaid leave" flag, which the question didn't ask about, so I left them out of the answer.
