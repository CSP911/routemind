1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O2, value W2, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods - likely holds the answer" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table, need to confirm which is current for today's date 2026-09-21" --member /v1/nodes/sec-supplier-due-diligence "overview of how due diligence pages fit together, may clarify terms like premises visit / file review"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9d1404 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body

2. **Answer**: No, a site visit is not required. The file (screening) is re-reviewed every 24 months. (For reference, this row also requires a screening score of at least 52 and last year's financial statements.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is current for today's date, 2026-09-21)
- /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body (the actual answer: site visit = no, re-review interval = every 24 months)

4. **Notes**: The procurement table lists three different due-diligence pages (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no date visible until you open the legend-revision page — picking the wrong one would have been an easy, silent mistake since the table listing alone doesn't flag that older versions are still live and undated in the top-level listing. The legend-revision page confirms three qualifiers (origin/value/goods) is the marker of the current table, which matched the row I used, so I did not need to open the goods/origin/value legend pages themselves. I opened the O2/W2/K3 row address directly (it was already printed in the initial overlay listing from the sec-hard-diligence table expansion) rather than first running `overlay add` for it — the close command noted this as "reached ... from somewhere the overlay never named" rather than an error, but worth flagging: the row I actually used was never explicitly added as a member before reading it.
