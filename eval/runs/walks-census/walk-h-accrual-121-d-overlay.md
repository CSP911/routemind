1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T3, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual and carryover cap questions live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d9fc02 --outcome answered --used /v1/regions/attendance /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body

2. **Answer**: For type E2, tenure T3, site L2 (current table, in force from 2026-01-01): accrues 0.90 days per month; carry-over limit is 11 days — that is the most you can still be holding into January. (Notice required to use it: 4 working days. It does not accrue during unpaid leave.)

3. **Source**:
- /v1/regions/attendance
- /v1/nodes/hard-accrual-legend-revision/body
- /v1/nodes/sec-hard-accrual
- /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body

4. **Notes**: The revision-legend page is the thing to check before trusting any accrual figure — this subject has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and the oldest version gives no indication it was ever superseded. Since today's date (2026-09-20/21) falls after 2026-01-01, the current table (`sec-hard-accrual`) applies, but grabbing the first accrual-looking row without checking the revision page would have risked picking a superseded version by mistake. The question already gave the row's qualifiers as exact codes (E2/T3/L2), so there was no need to consult the site/tenure/type legends to translate descriptive terms into codes. I read "how much can I still be holding in January" as asking for the carry-over limit (11 days) rather than a separate January-specific figure — the table has no month-specific carryover rule beyond the single carry-over limit, so that's the only figure that answers it.
