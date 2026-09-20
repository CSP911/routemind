1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body

2. Answer: No site visit is required. The vendor's file is re-reviewed every 36 months.

3. Source (in order used):
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body (the answer: site visit no, re-review every 36 months)

4. Notes: The procurement area's table listing flags up front that supplier due diligence has three superseded versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns that reaching for the newest is wrong for dates before 2026-01-01 — easy to skip that check and grab the wrong table by reflex. Today's date (2026-09-20) falls under the current table, `sec-hard-diligence`, so no correction was needed here, but it would have been for anything dated in 2025. All three qualifiers (origin, value, goods) happened to match a legend row's left-hand column exactly ("a vendor in Austin", "eight million won", "a licence"), so no nearest-entry judgment call was needed — worth flagging only because the legends explicitly allow for approximation when there's no exact match, and a careless reader could apply that fallback unnecessarily here. No other ambiguity encountered.
