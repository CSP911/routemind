1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E3, tenure T4, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site" --member /v1/nodes/hard-accrual-legend-revision/body "warns which accrual version covers which dates"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_fa1d45 --outcome answered --used /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
For type E3, tenure T4, site L1 (current table, in force from 2026-01-01): accrues 1.28 days per month, with a carry-over limit of 13 days — that is the most that can still be held over into January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body
/v1/nodes/hard-accrual-legend-revision/body (confirms today's date falls under the current, 2026-01-01-onward version, not one of the two superseded ones)

4. **Notes**
The attendance area lists three accrual pages (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, and the legend-revision page warns that the oldest one never states it was superseded — reaching for it by name alone would silently give a wrong-era answer. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct, but I checked the legend explicitly rather than assuming. The row itself directly answers both halves of the question — "accrues per month" and "carry-over limit" — with no need to combine separate documents, so this was a clean, single-row lookup once the right table was found.
