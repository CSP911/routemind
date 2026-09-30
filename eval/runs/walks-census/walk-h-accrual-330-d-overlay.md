1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T4, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "monthly accrual and carryover cap by type/tenure/site are leave policy topics"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a382a0 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body

2. **Answer**:
For type E4, tenure T4, site L1 (current table, in force from 2026-01-01):
- Accrues 1.60 days per month.
- Carry-over limit is 13 days — that is the most that can still be held (e.g. going into January).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual table versions applies to today's date, 2026-09-20/21)
- /v1/nodes/sec-hard-accrual (current accrual table index, located the exact E4/T4/L1 row)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body (the figures: 1.60 days/month accrual, 13 days carry-over limit)

4. **Notes**:
There are three versions of the leave accrual document (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for any date before 2026-01-01, and that the oldest version says nothing about being superseded — so skipping the version check would be an easy way to silently use stale figures. Today's date (2026-09-20) falls under the current table, so that risk didn't materialize here, but it's the kind of question where checking the date-to-version mapping first is not optional. The question's "how much can I still be holding in January" phrasing maps directly onto the row's "Carry-over limit, days" field — this table doesn't have a separate January-specific figure, so I read the carry-over limit as the answer to that half of the question. The type/tenure/site codes given in the question (E4, T4, L1) matched the row-indexing codes exactly, so I did not need to open the legend files that translate plain-language descriptions into those codes.
