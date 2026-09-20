1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row, not asked but on the same document: screening score required 45; financial statements — last three years, audited.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which version's dates apply)
/v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body (the answer)

4. **Notes**
The near-miss here is the version trap: `/v1/regions/procurement` lists three due-diligence documents side by side — the old `supplier-due-diligence`, the superseded `hard-diligence-v2` (2024-07-01 to 2025-12-31), and the current `sec-hard-diligence` (2026-01-01 onward) — with no obvious flag on which one is live. It would be easy to grab the first plausible-looking due-diligence table without checking dates. The `hard-diligence-legend-revision` document exists specifically to force that check, and it explicitly warns that reaching for the newest is wrong for anything before 2026-01-01 — today (2026-09-20) falls safely in the current version's range, so `sec-hard-diligence` was correct, but this is clearly a spot designed to trip up a careless walk. Once on the current table, the row for O1/W4/K4 was listed explicitly (three-qualifier indexing, no legend lookups needed since the codes were already given), so the rest of the walk was direct with no ambiguity.
