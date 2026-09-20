1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(For reference, this row also requires a screening score of 44 and audited financial statements for the last three years.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body

4. **Notes**
The procurement region table flags upfront that supplier due diligence has THREE versions (a `hard-diligence-legend-revision` warning, plus a superseded `hard-diligence-v2` and an even older `supplier-due-diligence`) — easy to grab a stale one by mistake. I went straight for `/v1/nodes/sec-hard-diligence`, which is explicitly labeled "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01," and today's date (2026-09-20) falls inside that range with no end date given, so it's current. The row itself confirms it's "in force from 2026-01-01" and names the prior versions, which matched the table listing — no discrepancy found. Since the question already gave codes (O1/W4/K3) rather than plain-language descriptions, I didn't need the legend files (origin/value/goods) to translate anything, which saved a step but is worth flagging in case the codes in the question weren't meant literally.
