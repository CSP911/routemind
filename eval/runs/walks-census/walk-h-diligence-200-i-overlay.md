1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Austin vendor, KRW 8,000,000, office consumables: site visit required? re-review frequency?" --member /v1/regions/procurement "vendor diligence / site visit / re-review cadence would be under procurement"
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a21baa --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body

2. **Answer**: No, a site visit is not required. The vendor's file is re-reviewed every 36 months.

3. **Source**:
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body (Site visit: no; Re-review interval: every 36 months)

4. **Notes**: All three inputs (origin, value, goods) mapped to exact legend entries — no nearest-band judgment calls needed, so no ambiguity there. The one thing worth flagging: the diligence table area carries an explicit warning that there are THREE versions of supplier due diligence in play (`hard-diligence-legend-revision`, superseded `hard-diligence-v2` for 2024-07-01 to 2025-12-31, and older `supplier-due-diligence`). I used `sec-hard-diligence`, which states it is in force from 2026-01-01, and today is 2026-09-20/21, so it's the correct live version — but it would be easy to grab the superseded `hard-diligence-v2` by mistake since the table listing surfaces multiple similarly-named diligence nodes side by side (including a legend-revision warning page and an overview/where-to-start page) that aren't the actual row data. Also did not need the approval-threshold tables at all — those answer approval routing, not site-visit/re-review, and the question doesn't ask about approval, so I left that thread alone.
