1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T2, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual per month and carry-over/holding cap are attendance topics"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0df2e0 --outcome answered --used /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body

2. **Answer**: For type E1, tenure T2, site L1 (current table, in force from 2026-01-01): accrues 0.48 days per month, and the carry-over limit — the most you can still be holding — is 7 days.

3. **Source**: /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body

4. **Notes**: The attendance area's working set surfaced a legend-revision warning that leave accrual has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), each indexed differently — checking that first was necessary to avoid grabbing the superseded `hard-accrual-v2` two-qualifier table instead of the current three-qualifier one. Since today's date (2026-09-20) falls after 2026-01-01, the current `sec-hard-accrual` table was the right one, and the question already gave exact codes (E1/T2/L1) so no legend lookups for type/tenure/site were needed. The only mild ambiguity was interpreting "how much can I still be holding in January" as the row's "carry-over limit" — the table doesn't call out January specifically, but carry-over/holding-over is what that limit governs, and no other figure in the row fits that phrasing.
