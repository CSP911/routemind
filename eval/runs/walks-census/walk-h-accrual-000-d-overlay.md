1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T1, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap questions belong under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b51494 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body

2. **Answer**:
For type E1, tenure T1, site L1 (current table, in force from 2026-01-01): accrues 0.40 days per month. The carry-over limit is 4 days — that is the most that can still be held going into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirms which version applies for today's date)
/v1/nodes/sec-hard-accrual (current accrual table, in force 2026-01-01 onward, listing the E1/T1/L1 row)
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body (the row itself: 0.40 days/month accrual, 4-day carry-over limit)

4. **Notes**:
Leave accrual has three superseded/current versions indexed by date (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns the oldest version says nothing about being replaced — reaching for it without checking the date would silently give a wrong, out-of-date figure. Today's date (2026-09-20) falls after the 2026-01-01 cutover, so `sec-hard-accrual` was the correct table; this was worth deliberately confirming rather than assuming "newest = current" is always right (the legend page says exactly that assumption fails for 2025-dated questions).

The question's "how much can I still be holding in January" reads oddly out of context, but maps directly onto the row's "Carry-over limit" field — the cap on days still held once the new year begins. No separate January-specific rule exists; the carry-over limit *is* the January-holding figure.

Since E1/T1/L1 was given explicitly and matched an exact row address in the table listing, there was no need to consult the site/tenure/type legend documents to decode ambiguous qualifiers — going straight to the named row was correct and saved a hop.
