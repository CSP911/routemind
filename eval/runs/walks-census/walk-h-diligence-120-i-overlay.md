1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 300,000,000 contract, office consumables: site visit required? review frequency?" --member /v1/nodes/sec-supplier-due-diligence "overview page ties together the due diligence pages" --member /v1/nodes/sec-hard-diligence "current due diligence table by origin, value, goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns which version covers which dates, need to confirm current version applies to 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f10bc5 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Screening score required: 54; financial statements: last two years — supporting context for the same row.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body — confirms today (2026-09-21) falls under the current (2026-01-01 onwards) version, `sec-hard-diligence`, not the superseded ones
/v1/nodes/hard-diligence-legend-origin/body — Stuttgart → origin O2
/v1/nodes/hard-diligence-legend-value/body — three hundred million won → value W3
/v1/nodes/hard-diligence-legend-goods/body — just office consumables → goods K1
/v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body — the row itself: site visit yes, re-review interval every 12 months

4. **Notes**
The procurement table lists three due-diligence documents with near-identical names (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and a legend-revision page exists specifically to warn against grabbing the wrong one — it flags that the oldest page never mentions it was superseded, so guessing from the page content alone would silently give a wrong-dated answer. Checked today's date (2026-09-21) against that page before touching any figures; it falls after 2026-01-01, so the current table (`sec-hard-diligence`, three-qualifier indexing) applies, not the two older versions.
The three legends (origin, value, goods) are the only place the mapping from plain-language facts to the O/W/K codes is written — the row pages don't repeat it — so all three had to be read before the row address could even be constructed correctly (Stuttgart=O2, three hundred million won=W3, just office consumables=K1). No ambiguity in the mapping itself; each legend had an exact match for the terms in the question.
