1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body

2. **Answer**: No, a site visit is not required. The file is re-reviewed every 24 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
/v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
/v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body (Site visit: no; Re-review interval: every 24 months)

4. **Notes**: The procurement table lists three due-diligence vintages side by side — a legend-revision warning page, a superseded `hard-diligence-v2` (2024-07-01 to 2025-12-31), and the current `sec-hard-diligence` (in force from 2026-01-01). Today is 2026-09-20, so the current table applies, but it would be easy to grab the superseded v2 row by mistake since both appear in the same listing with similar names. I also initially followed `supplier-due-diligence/body` (the older one-time-gate narrative page) expecting it to hold the site-visit/re-review answer — it doesn't; that information only lives in the coded row table (`sec-hard-diligence`), reached via three separate legend lookups (origin, value, goods) that must each be resolved before the row address can be constructed. The row's own footer confirms its effective date range and points back to the superseded versions, which is a useful cross-check that the right table was used.
