1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Regular payroll, 8 months tenure, Seoul office: monthly leave accrual rate, and max leave balance holdable in January" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - directly answers monthly accrual" --member /v1/nodes/annual-leave "entitlement and booking procedure, may cover carryover/cap rules for holding leave into January"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d3f622 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body

2. **Answer**: Accrues 0.40 days per month. Carry-over limit is 4 days — that is the most that can still be held once January comes.

3. **Source**:
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body

4. **Notes**: The three qualifiers ("regular payroll", "eight months", "Seoul office") each needed a separate legend lookup to translate into the row key (E1/T1/L1) — the accrual table itself never states these mappings, so guessing a row address directly would have been wrong even though the phrasing lines up almost word-for-word with the legend rows. All three translated to an exact match (no nearest-band guessing needed). I nearly widened the overlay to also read the general `annual-leave`/`leave-accrual` tables, but those are explicitly the older, superseded pages per the attendance table's own description ("current table since 2026-01-01" belongs to `sec-hard-accrual`) — `sec-hard-accrual` and its E1/T1/L1 row were the only current source needed. One oddity: the overlay close reported the four addresses I used as "reached ... from somewhere the overlay never named" — I had only added the parent tables (`sec-hard-accrual`, `annual-leave`) as overlay members, not the individual legend/row files I drilled into, so the tool flagged them as outside the named member set even though they were the correct answer.
