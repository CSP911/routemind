1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T4, site L2, monthly accrual rate and max carry/hold into January" --member /v1/regions/attendance "leave accrual and carryover rules by employee type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b6e0fd --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body

2. **Answer**:
Under the current leave accrual table (in force from 2026-01-01), for type E1, tenure T4, site L2: accrues 0.66 days per month, with a carry-over limit of 14 days — that is the most you can be holding when carrying into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body

4. **Notes**:
The tricky part was the version check, not the lookup itself: `sec-hard-accrual` is explicitly flagged as "THE CURRENT LEAVE ACCRUAL TABLE, in force from 2026-01-01" and there's a dedicated legend-revision page warning that the same subject has three versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with different date ranges, and that reaching for the newest is wrong for anything dated before 2026-01-01. Today's date (2026-09-20/21) is safely inside the current version's range, so this wasn't actually ambiguous, but the walk was built to make you check that rather than assume — worth flagging that a question dated in 2025 would need `hard-accrual-v2` instead. Once in the current table, the row for E1/T4/L2 exists exactly as named, so no legend disambiguation of the type/tenure/site codes was needed — a lucky direct hit. The "how much can I still be holding in January" phrasing maps to "Carry-over limit, days" on the row, not a separate January-specific figure; there is no other field that speaks to a January cap.
