1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dinner with a client, about 40 million won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount+term threshold likely determines signer and whether competitive quotes are required" --member /v1/regions/approval "approval chain / who can sign off may be detailed here" --member /v1/regions/expense "client entertainment dinner could be governed by expense rules"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m3/body
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3fc621 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m3/body /v1/nodes/hard-moved-threshold/body

2. **Answer**: The division director signs it off. Yes — three competing quotes and a written comparison are required first. (Delegation limit for this row is 100,062 thousand KRW; 13 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body
- /v1/nodes/hard-threshold-legend-amount/body
- /v1/nodes/hard-threshold-legend-term/body
- /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m3/body
- /v1/nodes/hard-moved-threshold/body

4. **Notes**: "Dinner with a client" maps exactly onto the category legend's own example (category C4), and "about 40 million won" / "locked in for three years" map exactly onto the amount (V4) and term (M3) legend examples — no interpolation needed, which is unusual and worth flagging as a possible tell that this question was built directly from those legend rows. The one real trap was the approval region: it still lists a `hard-moved-threshold` warning saying spend approval thresholds moved out of approval and into procurement's `sec-hard-threshold` as of 2026-01-01, and that the old approval-region rule (`delegation-scope`) is only correct before that date. Today is 2026-09-21, so I confirmed I had to use the procurement table and not anything in the approval region. There are also three superseded versions of the threshold table (`threshold-table`, `hard-threshold-v2`, and the current `sec-hard-threshold`) — easy to grab the wrong one if you don't check the effective-date note on the row itself, which confirms `sec-hard-threshold` is in force from 2026-01-01 and covers today.
