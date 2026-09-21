1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, about 40 million won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount/term threshold by category determines approval level and whether competitive quotes are required" --member /v1/regions/approval "whose signature is needed depends on the approval chain rules"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_148c9c --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body
```

2. **Answer**
The division director signs it off. Yes — three competing quotes plus a written comparison are required before it can be signed. (Delegation limit for this row is 100,046 thousand KRW; expect 13 working days.)

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (flights and hotels → category C3)
- /v1/nodes/hard-threshold-legend-amount/body (about 40 million won → amount V4)
- /v1/nodes/hard-threshold-legend-term/body (locked in for three years → term M3)
- /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body (the row itself: signer, quotes required)

4. **Notes**
- The question maps cleanly onto the three legends' example phrasing almost word-for-word ("flights and hotels", "about 40 million won", "locked in for three years"), so there was little risk of picking the wrong band — but it's easy to miss that all three legends have to be read before the row address can even be built, since the row addresses are only discoverable once you know C3/V4/M3.
- There are three historical versions of this threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page is explicit that reaching for the newest is only correct for dates in 2026 — a question without an explicit date could tempt you to skip that check. I confirmed today's date (2026-09-21) falls in the current table's 2026-01-01+ range before trusting the row.
- The procurement region table also surfaces a `hard-moved-threshold` warning noting thresholds moved from approval to procurement on 2026-01-01 — worth knowing this lives under procurement now, not approval, in case a future question is phrased around "who approves" rather than "who signs."
- The overlay close reported these four addresses as "reached" rather than as named members, since I read the table/legend/row files directly instead of adding each as an explicit overlay member first — functionally the same evidence trail, just a different bookkeeping path through the tool.
