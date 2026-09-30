1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T3, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and cap/carryover by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_122480 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body

2. **Answer**:
Accrues 1.56 days per month. Carry-over limit (the most you can still be holding when the new year turns over, i.e. into January) is 12 days.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual-table versions applies to today's date)
- /v1/nodes/sec-hard-accrual (the current, in-force-from-2026-01-01 table; located the E4/T3/L3 row)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body (the actual figures)

4. **Notes**:
Leave accrual exists in three versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with the same shape of content but different figures, and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version doesn't announce it's been superseded. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so that was the correct pick, but it's the kind of question where grabbing the first "leave accrual" hit without checking the revision legend would have silently given wrong numbers — worth flagging since a mid-2025-dated question would need `hard-accrual-v2` instead. The mention of "January" in the question maps to the row's "carry-over limit" field — there's no separate January-specific figure, so I read it as the cap on days still held into the new year, which is what a carry-over limit means.
