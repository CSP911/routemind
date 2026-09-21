1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Vendor in Austin, KRW 300M, office consumables only: is an on-site premises visit required, and how often is the file reviewed again?" --member /v1/nodes/sec-hard-diligence "current due diligence table, in force since 2026-01-01 - likely holds the site-visit and review-frequency rules by origin/value/goods" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together - may clarify which page governs review cadence" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence rules - need to confirm which applies as of 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_4a7b95 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
/v1/nodes/hard-diligence-legend-value/body (300 million won → value W3)
/v1/nodes/hard-diligence-legend-goods/body (office consumables → goods K1)
/v1/nodes/hard-diligence-legend-revision/body (confirms the three-qualifier current table applies for a 2026-09-20 question)
/v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body (row O3/W3/K1: site visit yes, re-review every 12 months)

4. **Notes**: The procurement table lists three versions of the due-diligence rules superseding each other (pre-2024-07-01, 2024-07-01–2025-12-31, and current since 2026-01-01), each indexed by a different number of qualifiers (one, two, three respectively). It would have been easy to grab the current table without checking the date, which happens to be correct here (today is 2026-09-20, so the three-qualifier current table `sec-hard-diligence` applies) — but the legend-revision page explicitly warns that a 2025-dated question would need the middle version instead, so that check was necessary rather than a formality. The three qualifiers (origin, value band, goods category) each require their own legend lookup and are not obvious from the question's plain-language phrasing — "three hundred million won" only maps to "W3" via the value legend, not by any arithmetic. No ambiguity in the final row: both the site-visit flag and the re-review interval are stated directly and unconditionally.
