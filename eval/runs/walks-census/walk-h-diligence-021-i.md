1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body

2. Answer
Yes, a site visit is required. The file gets re-reviewed every 12 months.
(Row: origin O1 / value W3 / goods K2 — screening score required 39, financial statements for the last two years, site visit yes, re-review interval every 12 months.)

3. Source
/v1/nodes/hard-diligence-legend-origin/body (Daejeon → O1)
/v1/nodes/hard-diligence-legend-value/body (three hundred million won → W3)
/v1/nodes/hard-diligence-legend-goods/body (something made to our spec → K2)
/v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body (final answer)

4. Notes
- The region table for procurement doesn't mention "site visit" at all in its description; the trail only becomes obvious once inside procurement, where "sec-hard-diligence" is explicitly flagged as THE CURRENT table by origin/value/goods.
- Nearly went down a dead end: /v1/nodes/supplier-due-diligence/body (the older, general due-diligence page) looks like a strong match by name and covers "the three checks," but it has nothing about site visits or re-review cadence — that detail only lives in the coded row table (sec-hard-diligence), not the narrative page. Same trap applies to sec-supplier-due-diligence/body, which is just an index/overview with no figures.
- The three legend lookups were all exact matches (Daejeon = O1 exactly, 300M won = W3 exactly, "made to our spec" = K2 exactly) — no fuzzy "nearest entry" judgment calls were needed here, which is unusual given the legends explicitly warn you might have to round.
- There's a superseded parallel table (hard-diligence-v2, in force 2024-07-01 to 2025-12-31) and a warning page (hard-diligence-legend-revision) flagging three historical versions of this same table. Since today is 2026-09-20 and sec-hard-diligence states it's in force from 2026-01-01 with no end date, it's clearly current — but a careless reader could easily grab the v2 numbers if not checking dates.
