1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "A couple of laptops, about 700,000 won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, likely has the answer by category/amount/term" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions - need to confirm which is current for today's date" --member /v1/nodes/purchase-request "purchase request process may cover quote requirements"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_869466 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body

2. **Answer**: The department head signs it off. No competing quotes are needed. (Delegation limit for this row is 1003 thousand KRW; working days to expect: 5.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body
- /v1/nodes/hard-threshold-legend-category/body
- /v1/nodes/hard-threshold-legend-amount/body
- /v1/nodes/hard-threshold-legend-term/body
- /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body

4. **Notes**: The three qualifiers in the question map cleanly onto the three legend tables' example rows almost verbatim ("a couple of laptops" → C1, "about 700,000 won" → V1, "until we cancel it" → M4), which made this feel almost too easy — worth double-checking that wasn't a coincidence, but the legends are explicit that these are the intended mappings. The one place I could have gone wrong was the revision warning: the threshold subject has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the warning explicitly says reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version doesn't announce it was superseded. Today's date (2026-09-21) is safely inside the current version's range (2026-01-01 onward, indexed by three qualifiers), so `sec-hard-threshold` / the row addresses under it were correct, but I made sure to check the revision legend before reading any row rather than assuming the current table applied.
