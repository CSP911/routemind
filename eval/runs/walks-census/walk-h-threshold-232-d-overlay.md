1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C3, amount V4, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount, term - matches procurement signature/quote question"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_98ca67 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body

2. **Answer**: Signs it off: the division director. Competing quotes required: yes — three and a written comparison. (Delegation limit for this row: 100046 thousand KRW; working days to expect: 13.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions is current for today's date)
- /v1/nodes/sec-hard-threshold (current table index, listing the row for this exact category/amount/term combination)
- /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body (the actual figures)

4. **Notes**: The procurement region has three separate versions of the approval-threshold document (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns explicitly that reaching for the newest is wrong for any date before 2026-01-01. Today (2026-09-21) falls in the current table's range, so `sec-hard-threshold` was correct, but this is an easy trap for older-dated questions — worth double-checking the in-force date every time rather than assuming "current" is always right. Otherwise the walk was direct: the row address for C3/V4/M3 existed exactly as named in the table listing, no ambiguity in category/amount/term codes.
