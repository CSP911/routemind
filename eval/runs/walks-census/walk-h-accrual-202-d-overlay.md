1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T1, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carryover cap are attendance/leave topics"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9c8d5a --outcome answered --used /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body

2. **Answer**
Accrues 1.08 days per month. Carry-over limit (the maximum balance you can still be holding into January) is 6 days.

3. **Source**
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body

4. **Notes**
The type/tenure/site codes in the question (E3, T1, L3) matched a row in the current accrual table exactly, so no legend lookup was needed to translate plain-language descriptions into codes. Worth flagging: this table has three superseded versions (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual` in force from 2026-01-01), noted via `hard-accrual-legend-revision`. Today's date (2026-09-21) falls inside the current version's range, so no ambiguity there, but it would be easy to grab a stale version's row by mistake if not careful. The row itself doesn't use the phrase "carry-over into January" — it just states "Carry-over limit, days: 6" — I'm reading that as answering "how much can I still be holding in January," which is the standard meaning of a leave carry-over cap, but the row doesn't spell out "January" explicitly.
