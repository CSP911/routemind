1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T2, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carryover/cap questions live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7bbb3e --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body

2. **Answer**:
For type E2, tenure T2, site L3: accrues 0.84 days per month. The carry-over limit is 9 days — that is the most you can still be holding into January.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual table versions is in force for today's date, 2026-09-20/21)
- /v1/nodes/sec-hard-accrual (the current accrual table, in force from 2026-01-01, used to locate the exact row)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body (the row with the figures: 0.84 days/month accrual, 9-day carry-over limit)

4. **Notes**:
The main risk here was the three-versions trap: RouteMind has three separate documents for leave accrual (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, and the legend-revision page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01. Since today is 2026-09-20/21, the current table (`sec-hard-accrual`, in force from 2026-01-01) is correct, but I checked the revision-legend page first rather than assuming. The E2/T2/L3 row was listed directly and unambiguously once the table was opened, so no legend lookup for the type/tenure/site codes was needed — the row title itself confirmed the match. No ambiguity remained once the correct table version was confirmed.
