1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body

2. **Answer**
For type E4, tenure T2, site L3 (current table, in force from 2026-01-01):
- Accrues per month: 1.48 days
- Carry-over limit (max you can still be holding into January): 9 days

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body (the answer)

4. **Notes**
The attendance table warns up front that leave accrual has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and current since 2026-01-01) and that the oldest version never says it was superseded — so checking the legend-revision page before trusting any accrual figure was necessary, not optional. Today's date (2026-09-20) falls under the current, three-qualifier table (`sec-hard-accrual`), so no ambiguity there. The question gave all three qualifiers (E4, T2, L3) directly, so the row address could be built confidently from the table listing without needing the type/tenure/site legend files. "How much can I still be holding in January" reads as the carry-over limit field on the row (9 days) rather than a separate January-specific rule — there is no other January-specific figure on this row, and nothing in the attendance area suggested a distinct year-end/January table for this subject.
