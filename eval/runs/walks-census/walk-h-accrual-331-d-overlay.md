1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T4, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rates and carryover/cap rules by employee type, tenure, and site"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9f8633 --outcome answered --used /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body

2. **Answer**
For type E4, tenure T4, site L2: accrues 1.62 days per month. The carry-over limit is 14 days — the most that can still be held (carried into January).

3. **Source**
/v1/nodes/sec-hard-accrual (table listing the row)
/v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body (the figures)

4. **Notes**
The table listed E1–E4 × T1–T4 × L1–L4 rows (64 total), and the exact E4/T4/L2 combination was present verbatim, so no interpolation or legend lookup was needed. The one thing worth flagging: there's a `hard-accrual-legend-revision` warning that leave accrual has three superseded versions (`leave-accrual`, `hard-accrual-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-accrual` for 2026-01-01 onward). I almost went to check the legend-revision node to be sure I had the right version, but the row document itself states "In force from 2026-01-01" and today is 2026-09-20/21, so the current table was already the right one — checking the legend would have been redundant. The "how much can I still be holding" phrasing maps to the "Carry-over limit" field; it isn't explicitly labeled as a January-specific figure, but the carry-over limit is what caps what you're holding going into the new year, so I read it as the same number.
