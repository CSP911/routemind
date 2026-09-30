1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W4, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "origin/value/goods codes and premises visit + review cycle sound like vendor due diligence under procurement"
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a1ad00 --outcome answered --used /v1/nodes/sec-hard-diligence/body /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**:
- /v1/nodes/sec-hard-diligence (table listing the current supplier due diligence rows, in force from 2026-01-01)
- /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body (the row itself, contributed the "Site visit: yes" and "Re-review interval: every 6 months" figures)

4. **Notes**: The area table's one-line hint for procurement didn't mention due diligence explicitly, but "origin/value/goods" in the question was distinctive enough to point straight at supplier due diligence. The bigger trap was version: the due-diligence rules have three historical versions (`supplier-due-diligence`, `hard-diligence-v2`, and the current one), each flagged with warnings in a legend-revision node. I went straight for `/v1/nodes/sec-hard-diligence`, which is explicitly labeled "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01" — since today is 2026-09-21, that's correctly the applicable version, and the row itself also restates that in-force date, so I didn't need to open the superseded versions or the legend-revision node to confirm it. Also note the origin/value/goods codes (O4, W4, K3) were given directly as codes in the question, so no legend lookup (origin/value/goods classification) was needed — the row address encodes them exactly.
