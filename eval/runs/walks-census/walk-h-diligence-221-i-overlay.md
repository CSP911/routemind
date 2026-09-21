1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Vendor in Austin, 300,000,000 KRW, custom-made-to-spec goods: is a site visit to the vendor's premises required, and how often is the vendor's file reviewed again?" --member /v1/regions/procurement "Question is about vendor site visits and vendor file re-review cadence for a custom-made purchase, which is procurement/vendor management territory"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5637d6 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body

2. **Answer**: Yes, a site visit to the vendor's premises is required. The vendor's file is re-reviewed every 12 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body

4. **Notes**: The question maps cleanly onto the legends with no fuzzy matching needed — "a vendor in Austin" is a listed exact entry (origin O3), "three hundred million won" is a listed exact entry (value W3), and "something made to our spec" is a listed exact entry (goods K2), so there was no ambiguity in picking the row and no need to fall back to "nearest entry above." The one place I paused was the due-diligence versioning warning (`hard-diligence-legend-revision` flags three versions of this table with different in-force windows). I checked the row's own footer, which states it is "in force from 2026-01-01" and names the two superseded versions (`hard-diligence-v2`, `supplier-due-diligence`); since today is 2026-09-20/21, the current `sec-hard-diligence` table is the right one and I didn't need to open the superseded versions or the legend-revision doc itself. Worth flagging: the overlay's working set never listed the specific legend/row addresses I ended up reading (only the parent table) — the close command accepted them anyway but tagged them "reached ... from somewhere the overlay never named," which is just how the tool records addresses found by drilling into a table row rather than declared as overlay members up front.
