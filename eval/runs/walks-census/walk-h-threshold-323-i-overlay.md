1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dinner with a client, around 12 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount, and term - open-ended/indefinite term contract fits 'until we cancel it'" --member /v1/regions/expense "client entertainment/dinner expense rules, receipts, corporate card"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b1d6bf --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m4/body

2. **Answer**: The division director must sign it off, and yes — three competing quotes are required. (Delegation limit 20,059 thousand KRW; 11 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body (dinner with a client → category C4)
- /v1/nodes/hard-threshold-legend-amount/body (around 12 million won → amount V3)
- /v1/nodes/hard-threshold-legend-term/body (until we cancel it → term M4)
- /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m4/body (the row itself: division director, three quotes)

4. **Notes**: The phrase "until we cancel it" reads like ordinary conversational filler, not a contract-term signal — easy to skim past and default to a one-off approval lookup. But the term legend spells it out verbatim as term M4 ("until we cancel it" = open-ended/evergreen commitment), so it was clearly meant to be picked up. I initially widened the working set to include the expense region (client entertainment/receipts) since "dinner with a client" sounds like a T&E claim, but the question is actually about the approval/procurement threshold for committing to an indefinite-term spend, not about how to file the receipt — the expense region rows were never used. The current threshold table (`sec-hard-threshold`, in force from 2026-01-01) applied directly since today is 2026-09-21; I did not need to touch the superseded `hard-threshold-v2` or the three-version legend-revision warning, but noticed them and would check there if the date were earlier.
