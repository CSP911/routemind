1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body

2. **Answer**: You accrue 1.64 days per month. The carry-over limit (the most you can still be holding into January) is 15 days. This does not accrue during unpaid leave, and any pre-approved excess needs 7 working days' notice.

3. **Source**: /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body

4. **Notes**: The attendance area's leave-accrual subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns not to reach for the newest table by reflex. Today's date (2026-09-20) falls after the 2026-01-01 cutover, so the current table (`sec-hard-accrual`) is correct here — but this is exactly the kind of question where grabbing the current table without checking the effective date first would have been a lucky guess rather than a verified one. The question already gave the row's three qualifiers as codes (E4/T4/L3), so no legend lookup for type/tenure/site was needed — the row matched directly in the table listing. "How much can I still be holding in January" reads as the carry-over limit (max balance retained into the new year), not a separate January-specific figure — the table has no month-specific breakdown beyond the flat monthly accrual rate and the single carry-over limit.
