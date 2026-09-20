1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k2/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (version selection)
/v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
/v1/nodes/hard-diligence-legend-value/body (700 million won → value W4)
/v1/nodes/hard-diligence-legend-goods/body (made to spec → goods K2)
/v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k2/body (site visit: yes; re-review interval: every 6 months)

4. **Notes**: The procurement table lists three supplier-due-diligence versions (oldest, v2, and current `sec-hard-diligence`), each superseding but not withdrawing the last, and the legend-revision page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-20) falls in the current version's range, so `sec-hard-diligence` was correct, but this was the one place it would have been easy to grab the wrong version if the question had been dated earlier — worth double-checking the in-force dates every time rather than assuming "current" is always right. The three legend tables (origin, value, goods) had to be resolved independently before the row address could be built — the row address itself is not discoverable without doing that mapping first; guessing at a row address would violate "never construct one," so all three legends were read before touching the row.
