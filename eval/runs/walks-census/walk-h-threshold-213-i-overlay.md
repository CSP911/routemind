1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, roughly 3 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount + open-ended term suggests procurement approval threshold table" --member /v1/regions/expense "flights and hotels are travel expense items"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e1b038 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body

2. **Answer**: The division director signs it off, and yes — two competing quotes are needed. (Delegation limit for this row is 5,039 thousand KRW; expect 8 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body — mapped "flights and hotels" to category C3
- /v1/nodes/hard-threshold-legend-amount/body — mapped "roughly 3 million won" to amount V2
- /v1/nodes/hard-threshold-legend-term/body — mapped "until we cancel it" to term M4
- /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body — the row itself, in force from 2026-01-01, current as of today (2026-09-21)

4. **Notes**: The question's exact phrasing ("roughly 3 million won", "until we cancel it") turned out to be lifted almost verbatim from the amount and term legends, which made the C3/V2/M4 lookup unambiguous once I found the legend files — no judgment call needed on banding. The one real fork was at the top: "flights and hotels" reads like a travel-expense question, so I opened both /v1/regions/expense and /v1/regions/procurement as members before narrowing. It's the procurement approval-threshold table (by category/amount/term) that actually answers "whose signature" and "how many quotes," not anything under expense — the expense region's tables (corporate travel agency, travel-expense, etc.) are about what the company reimburses, not who approves committing to it. Also worth flagging: the current threshold table explicitly supersedes two older versions (hard-threshold-v2 and threshold-table) reachable from the same table listing; I did not open those since the row I read states it's in force from 2026-01-01 and today is 2026-09-21, so the current row applies — but a careless walker could easily grab the superseded v2 row instead since it sits right next to the current one in the table listing with a similar name.
