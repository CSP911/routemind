1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/threshold-table/body

2. **Answer**: Under the version in force until 2024-07-01 (which covers March 2023), a purchase of 2,000,000 KRW net of VAT falls in the 500,000–3,000,000 KRW band: approval is by the **Division head, delegated**, requiring **2 quotes**.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (identifies which of the three threshold versions covers March 2023)
- /v1/nodes/threshold-table/body (the oldest approval threshold table, in force until 2024-07-01, containing the actual figures)

4. **Notes**: The procurement region's table only surfaces the two newer threshold versions (`hard-threshold-v2` for 2024-07-01–2025-12-31 and `sec-hard-threshold` as current since 2026-01-01) plus the legend page — the oldest version (in force until 2024-07-01, the one that actually covers March 2023) isn't listed there at all. The legend names it only as `threshold-table`, not a full address, and warns explicitly that "the oldest says nothing at all about having been replaced" — so reading that page alone would give no hint that a newer version exists or that it's the wrong one for a later date. I found the actual document by a different path: through /v1/nodes/purchase-request → /v1/nodes/approval-threshold → /v1/nodes/threshold-table/body. Had I not read the legend first and just grabbed the first threshold-looking table under /v1/regions/procurement, I'd likely have picked `hard-threshold-v2` (superseded but dated closer to today) or the current `sec-hard-threshold`, both wrong for March 2023.
