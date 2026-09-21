1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W3, goods K3, do we have to visit their premises, and how often does their file get reviewed again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision/body "warning about 3 versions of diligence table, need to confirm current one applies"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_aa0006 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body
/v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body

4. **Notes**: The procurement table lists three separate supplier-due-diligence versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with an explicit warning page saying the newest is not automatically the right one — a question dated in 2025 needs the middle version, not the current one. Today's date (2026-09-20) falls inside the current table's range (2026-01-01 onwards), so `sec-hard-diligence` and its per-row page were correct here, but this is the kind of question where grabbing the current table without checking the date would have been the wrong instinct on a different date. The row itself was a direct hit once the overlay expanded `sec-hard-diligence` into its full origin/value/goods grid — no ambiguity there, the O1/W3/K3 row was named exactly.
