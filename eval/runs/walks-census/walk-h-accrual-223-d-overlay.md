1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T3, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and max carryover/holding limits are attendance topics"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_8965fc --outcome answered --used /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**:
Accrues 1.26 days per month. Carry-over limit is 13 days — that is the most that can still be held over the year boundary into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**:
The accrual topic has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) each covering a different date range, and the legend-revision doc warns explicitly against "reaching for the newest" by reflex. Today's date (2026-09-20/21) falls after the 2026-01-01 cutover, so the current table (`sec-hard-accrual`) was the right one to use, but this is exactly the kind of question where grabbing the newest-looking table without checking the date would happen to be right for the wrong reason — a question dated in 2025 would need `hard-accrual-v2` instead. Worth flagging: the overlay close reported both sources as "reached" rather than matched against named members, because I only added the parent `/v1/regions/attendance` table as a working-set member and drilled into the specific row/legend files directly rather than adding each as its own member — didn't affect the answer, just a bookkeeping note.
