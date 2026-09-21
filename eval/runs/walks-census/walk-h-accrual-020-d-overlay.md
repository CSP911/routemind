1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T3, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover cap by employee type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0f03bc --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body

2. **Answer**:
Accrues 0.56 days per month. Carry-over limit (the most that can still be held) is 10 days. This is under the current leave accrual table, in force from 2026-01-01.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirms which of the three accrual table versions applies)
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body (the E1/T3/L1 row itself: 0.56 days/month, 10-day carry-over limit)

4. **Notes**:
The accrual subject has three superseding versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no note on the oldest ones saying they were replaced — the legend-revision page warns explicitly that reaching for the newest is wrong for any date before 2026-01-01. Today's date (2026-09-20/21) and the "January" in the question both fall after the 2026-01-01 cutover, so the current table (`sec-hard-accrual`) is correct here, but this was worth checking rather than assuming, since a question about an earlier date would need `hard-accrual-v2` instead. The "how much can I still be holding in January" phrasing is really asking about the carry-over limit, not a fresh entitlement — that wording could be misread as asking for a specific balance calculation, but the row only states the flat carry-over cap (10 days), which is the only figure the document base offers for that question.
