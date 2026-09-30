1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T4, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carryover cap by employment type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7bd404 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body

2. **Answer**: For type E3, tenure T4, site L4 (current table, in force from 2026-01-01): accrues 1.34 days per month. Carry-over limit is 16 days — that is the most you can still be holding.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three versioned tables applies to today's date)
/v1/nodes/sec-hard-accrual (table listing, used to locate the exact row)
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body (the figures)

4. **Notes**: The area is versioned three times over (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each covering a different date range, and the legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 and that the oldest version says nothing about being superseded. Today's date is after 2026-01-01, so the current table (`sec-hard-accrual`) is correct, but this was worth checking rather than assuming — the "always latest" instinct would have been right here only by luck. The question already gave type/tenure/site as codes (E3/T4/L4), so no legend lookup for translating a plain-language description into a code was needed — the row title matched directly. The carry-over limit is a static cap in the row (16 days), not a January-specific figure; I read "how much can I still be holding in January" as asking for that carry-over ceiling since the table has no separate month-by-month balance, only a monthly accrual rate and a single carry-over limit.
