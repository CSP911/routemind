1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T2, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_98ec4f --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body

2. **Answer**
Accrues 1.50 days per month. Carry-over limit (the most that can still be held) is 10 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body

4. **Notes**
Leave accrual has three versions in force over different date ranges (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns that the oldest version never mentions being superseded — grabbing the newest table without checking would have been fine here only by luck, since the question carries no date of its own and I had to anchor on today's date (2026-09-20/21) to justify using `sec-hard-accrual`, the table in force from 2026-01-01. Worth flagging: the row's carry-over limit field is the most natural reading of "how much can I still be holding in January," but the table never explicitly ties the carry-over limit to a January checkpoint — it's presented as a general cap, not a January-specific one. I'm reporting it as the answer to "how much can still be held" because that's what the field is, but the January framing in the question isn't independently confirmed in the source.
