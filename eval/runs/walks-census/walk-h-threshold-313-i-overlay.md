1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Dinner with a client, roughly 3 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, and term - need signature level" --member /v1/nodes/purchase-request "how many quotes are needed before approval" --member /v1/nodes/corp-card "entertainment cap and card use, since this is a client dinner" --member /v1/nodes/sec-spending-that-needs-a-draft-first "may need draft approval before spend if over cap"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_86b80a --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m4/body

2. **Answer**: The division director signs it off. Yes — two competing quotes are required. (Delegation limit for this row is 5,055 thousand KRW; 8 working days to expect.) This is the current table, in force from 2026-01-01.

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m4/body

4. **Notes**: "Dinner with a client" reads like an expense question, so the natural first stop is /v1/regions/expense — but that area's tables (corp-card, spending-that-needs-a-draft-first) only cover caps and pre-approval drafts, not signatures or quotes. The actual answer lives in /v1/regions/procurement, under /v1/nodes/sec-hard-threshold, which is a three-axis lookup (category × amount × term) rather than a single table — the phrasing "until we cancel it" is not obviously a procurement "term" until you read the term legend and see "until we cancel it" listed verbatim as M4. Missing that step would have led to guessing at a signature level from the expense side, which has none. The legend files explicitly warn the category/amount/term mapping is "the only place the mapping is written down" and rows don't repeat it, so all three legends had to be read before the row address could be built correctly. The overlay only had the parent table addresses as members (sec-hard-threshold, purchase-request, etc.); the individual matrix-row files it printed underneath were used directly without an explicit `overlay add`, so the close command reported them as "reached" rather than as named overlay members — worth noting since it means the overlay's own bookkeeping under-counts what was actually walked.
