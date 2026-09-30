1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T1, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carryover/cap questions live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d437a4 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body

2. **Answer**
For type E2, tenure T1, site L2 (current table, in force from 2026-01-01):
- Accrues 0.74 days per month.
- Carry-over limit is 5 days — this is the most you can still be holding when the year rolls into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirms which version applies for today's date, 2026-09-20)
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body (the figures)

4. **Notes**
Leave accrual has three versions covering different date ranges, and the legend page warns the oldest version says nothing about being superseded — so checking today's date against the legend before trusting any accrual table is a required step, not optional. Today (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`, three qualifiers: type/tenure/site) is the right one; the superseded `hard-accrual-v2` (2024-07-01 to 2025-12-31) would have been wrong here and was tempting to reach for since it's also indexed similarly. The E2/T1/L2 row was an exact, unambiguous match to the three qualifiers given in the question, so no legend lookup for type/tenure/site codes was needed beyond confirming they were already given as codes. I read "how much can I still be holding in January" as asking for the carry-over limit (the cap on balance held across the year boundary), since that's the only figure in this row about what you can hold rather than what you accrue — there's no separate "January" figure, so this is an inference, not a labeled field.
