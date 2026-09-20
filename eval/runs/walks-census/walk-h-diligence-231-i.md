## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body

## Answer
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also: screening score required is 75; financial statements must be the last three years, audited — noted for context though not asked.)

## Source
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (something made to our spec → goods K2)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body (site visit: yes; re-review interval: every 6 months)

## Notes
The procurement table surfaces three separate versions of the supplier due diligence page (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), each superseding the last but none marked withdrawn — the legend-revision page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-20) falls within the current version's range (2026-01-01 onward), so `sec-hard-diligence` was correct here, but this is an easy place to grab the wrong table on a differently-dated question.

The current table is indexed by three qualifiers (origin, value, goods) that only resolve to codes via three separate legend pages — "Austin," "seven hundred million won," and "something made to our spec" map to O3, W4, K2 respectively. All three legends state plainly they are "the only place the mapping is written down," so skipping them and guessing codes directly would have been a mistake. With 64 rows listed under `sec-hard-diligence`, the correct row address only became identifiable after all three lookups were done — it was among the addresses the table itself printed, just not findable without the codes in hand.
