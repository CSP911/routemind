1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T4, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py overlay add --id ov_2026-09-20_d0b4de --address /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body --why "exact row for E1/T4/L3 in the current accrual table"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d0b4de --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body

2. **Answer**: For type E1, tenure T4, site L3 (current table, in force from 2026-01-01): accrues 0.68 days per month, with a carry-over limit of 15 days — so up to 15 days can still be held over into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body

4. **Notes**: The main trap here is versioning, not lookup — the accrual subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20/21) falls after the current table's effective date (2026-01-01), so `sec-hard-accrual` was the correct version, but it would have been easy to skip that check and just grab whichever table looked newest without confirming the date actually fell inside its range. The question's "how much can I still be holding in January" maps directly onto the row's "Carry-over limit" field — there was no separate January-specific cap to find, and no other table in the working set (e.g. sec-days-that-decide-money) turned out relevant once the exact E1/T4/L3 row was located.
