1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T4, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carry-over cap by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_da68bd --outcome answered --used /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body

2. **Answer**:
For type E2, tenure T4, site L4: accrues 1.02 days per month. Carry-over limit (the most you can still be holding, e.g. going into January) is 16 days. (Accrual does not occur during unpaid leave; 3 working days' notice is required to use leave, though that wasn't asked.)

3. **Source**:
/v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body

4. **Notes**:
There are three versions of the leave accrual document (`leave-accrual`, `hard-accrual-v2` for 2024-07-01–2025-12-31, and `sec-hard-accrual` current from 2026-01-01), and a legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today is 2026-09-20/21, and the "January" in the question reads as the upcoming carry-over point, so the current table applies — no need to touch the superseded versions. This was the one place a careless read could have gone wrong (grabbing the newest table without checking the date), so I checked the revision-legend page first before reading the row. The row itself gave both figures directly under exact E2/T4/L4 labels with no further legend lookup needed since the question already used the row's own codes.
