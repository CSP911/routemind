1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body

2. **Answer**
Accrues 0.86 days per month. Carry-over limit is 10 days — that is the most that can still be held over into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date)
/v1/nodes/hard-accrual-legend-type/body (two-year contract → type E2)
/v1/nodes/hard-accrual-legend-tenure/body (been here two years → tenure T2)
/v1/nodes/hard-accrual-legend-site/body (fully from home → site L4)
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body (0.86 days/month accrual, 10-day carry-over limit)

4. **Notes**
The employment-type legend is the part most likely to trip someone up: "on a two-year contract" maps to E2, but the wording is close enough to "on the regular payroll" (E1) that a careless read could pick the wrong row — the legend note that this is "the only place the mapping is written down" is there for a reason. The revision-warning page mattered here too: there are three versions of this table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and today's date (2026-09-20) falls under the current one, `sec-hard-accrual` — but nothing on the table itself would have flagged that without reading the legend-revision page first, and the oldest version "says nothing at all about having been replaced," so skipping that check could silently give a superseded figure. The question's second half ("how much can I still be holding in January") reads like it could be asking about a separate year-end carryover procedure, but the row itself already contains a "Carry-over limit, days" field, so no separate carryover document was needed — I treated that field as the direct answer rather than searching further, which seems right given the table's own framing ("monthly accrual rate, the carry-over limit and the notice required").
