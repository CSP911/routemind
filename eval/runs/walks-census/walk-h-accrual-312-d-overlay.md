1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T2, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover cap by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d57445 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body

2. **Answer**: Accrues 1.48 days per month. Carry-over limit (the most you can still be holding) is 9 days. (In force from 2026-01-01; this row does not accrue during unpaid leave, and requires 7 working days' notice.)

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual (table, to find the E4/T2/L3 row)
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body

4. **Notes**: The attendance area holds three separate versions of the leave-accrual document (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each in force for a different date range, and the oldest one gives no indication it's been superseded. Checking `hard-accrual-legend-revision` first was necessary to confirm that today's date (2026-09-20/21) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01) rather than the superseded `hard-accrual-v2`. Without that check it would have been easy to grab a plausible-looking but wrong (pre-2026) figure. Once on the right table, the row for type E4/tenure T2/site L3 was an exact, literal match to the question's own codes — no legend translation needed. The question's "how much can I still be holding" maps to the table's "Carry-over limit" field.
