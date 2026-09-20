1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body

2. Answer:
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Origin: Daejeon = O1; Value: seven hundred million won = W4 exactly; Goods: "people's time" = K3 exactly — row O1/W4/K3.)

3. Source:
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → O1)
- /v1/nodes/hard-diligence-legend-value/body (700M won → W4)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → K3)
- /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body (site visit: yes; re-review interval: every 6 months)
- /v1/nodes/hard-diligence-legend-revision/body (confirms sec-hard-diligence, in force 2026-01-01 onwards, is the correct version for today 2026-09-20)

4. Notes:
The procurement table lists two competing "due diligence" areas: the overview page (/v1/nodes/sec-supplier-due-diligence) and the actual lookup table (/v1/nodes/sec-hard-diligence). The overview page reads like it will answer the question — it talks about ongoing checks and re-checking — but it's prose about the process philosophy, not the actual figures; it would have been easy to write an answer from it and miss the real numbers entirely. The real answer lives only in the indexed row table.

There are three versions of this table (supplier-due-diligence, hard-diligence-v2, sec-hard-diligence), and the revision-legend page explicitly warns not to default to the newest — a 2025-dated question would need hard-diligence-v2 instead. Today's date (2026-09-20) falls after the 2026-01-01 cutover, so the current three-qualifier table was correct here, but this was a genuine place to go wrong if the date weren't checked.

All three inputs (Daejeon, 700 million won, "people's time") mapped to their codes exactly, with no need to round to a nearest band — a cleaner walk than the legends' "nearest entry" fallback language implies is typical.
