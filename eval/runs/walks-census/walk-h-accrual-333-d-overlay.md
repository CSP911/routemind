1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T4, site L4: monthly leave accrual rate and January carryover cap" --member /v1/regions/attendance "leave accrual and carryover rules by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_06536d --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body

2. **Answer**:
Accrues 1.66 days per month. Carry-over limit is 16 days — that is the most you can still be holding into January (any excess not approved in advance is forfeited; an unavoidable excess needs a short written statement and is decided by the budget holder).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual-table versions applies for today's date)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body (the figures: 1.66 days/month accrual, 16-day carry-over limit)

4. **Notes**:
This subject has three superseded versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page is explicit that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so no version confusion applied here — but it's the kind of check that's easy to skip, and the table would give a plausible-looking wrong number if the wrong version were read. The row address matched the E4/T4/L4 qualifiers directly with no legend translation needed since the question already used the table's own codes. "How much can I still be holding in January" maps to the row's "Carry-over limit, days" field — the table doesn't use the word "January" anywhere, so that phrasing took a moment to connect to the right field.
