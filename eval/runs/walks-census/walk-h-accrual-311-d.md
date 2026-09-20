1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body

2. **Answer**
For type E4, tenure T2, site L2: accrues 1.46 days per month. Carry-over limit (the most you can still be holding, e.g. going into January) is 8 days.

3. **Source**
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body

4. **Notes**
The attendance area lists three versions of the leave accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and a warning page explicitly says the oldest version gives no indication that it was ever superseded — so picking the current table by name alone would have been a guess. Checked `hard-accrual-legend-revision` first to confirm today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), which also matches the "carry-over" wording in the question ("how much can I still be holding in January") — that phrase maps to the "Carry-over limit" field in the row, not a separate document. The E4/T2/L2 row was directly listed in the table's index, so no legend lookups for type/tenure/site codes were needed since all three were given as codes already.