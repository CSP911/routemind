1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T2, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual per month and carry-over/holding cap by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_59b077 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body

2. **Answer**:
For type E3, tenure T2, site L2 (current table, in force since 2026-01-01):
- Accrues 1.14 days per month.
- Carry-over limit (what can still be held into January) is 8 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body

4. **Notes**:
Leave accrual has three versions by date, and the legend page warns the oldest version says nothing about being superseded, so grabbing the first "leave accrual" hit without checking dates would silently give a wrong (older) rule. Today's date (2026-09-20/21) falls after 2026-01-01, so the current table `sec-hard-accrual` is the right one — I checked the revision-legend page before trusting that. The row for E3/T2/L2 existed directly, indexed by exactly the three qualifiers given in the question, so no legend lookup for what "E3"/"T2"/"L2" mean was needed. The phrase "how much can I still be holding in January" maps to the table's "carry-over limit" field — nothing in the row is labeled specifically for January, so this is an inference that carry-over limit is the holding cap that persists into the new year, not a distinct January-specific figure.
