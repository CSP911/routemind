1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body

2. **Answer**
Site visit: no. Re-review interval: every 24 months. (Also on file: screening score required 68, financial statements from the last year.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body
(consulted for version-currency: /v1/nodes/hard-diligence-legend-revision/body)

4. **Notes**
The procurement area has three separate versions of the supplier due-diligence table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that grabbing the newest one is wrong for older dates. Today's date (2026-09-20) falls in the current version's range, so `sec-hard-diligence` was correct, but this is an easy place to go wrong if the date check is skipped. The question already gave the row qualifiers as codes (O3, W2, K3) rather than plain-language descriptions, so no legend lookup was needed to translate a company/location/goods description into a code — I only opened the legend-revision page to confirm which table version applies. The row's "If the figures are exceeded" boilerplate paragraph looks like it was copy-pasted from an expense/travel-limits page and has nothing to do with site visits or review intervals — worth flagging as a documentation inconsistency, but it didn't affect the answer.
