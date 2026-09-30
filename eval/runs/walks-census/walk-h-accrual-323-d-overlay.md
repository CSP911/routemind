1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T3, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carryover/holding cap for leave are attendance topics"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_37bc3e --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body

2. **Answer**: For type E4, tenure T3, site L4: accrues 1.58 days per month; carry-over limit is 13 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body

4. **Notes**: The accrual table exists in three versions with different date ranges (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend page warns that reaching for the newest is wrong for anything before 2026-01-01. Today's date (2026-09-20/21) falls in the current version's range, so `sec-hard-accrual` was the correct table — but this was the point where it would have been easy to grab the wrong version without checking. The "how much can I still be holding in January" phrasing maps to the row's carry-over limit (13 days); the table itself doesn't spell out a January-specific rule beyond that field, so I'm reading it as the standing carry-over cap rather than a separate January-only figure — there was no other January-specific note in the row to point to.
