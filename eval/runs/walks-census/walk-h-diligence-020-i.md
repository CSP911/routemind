1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months. (Also required, though not asked: screening score of 38, and financial statements for the last two years.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → O1)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → W3)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → K1)
- /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body (final answer: site visit yes, re-review every 12 months)

4. **Notes**: The procurement region table lists a `hard-diligence-legend-revision` warning up front stating this subject has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and that "reaching for the newest is wrong for anything before 2026-01-01" — with the oldest version giving no indication it was ever superseded. Today's date (2026-09-20) falls under the current table (`sec-hard-diligence`, in force since 2026-01-01), so this was a straightforward case, but it would have been easy to skip the revision check entirely and just grab the current table without confirming the date actually falls in its range — the warning is explicit that assuming "newest" is the trap. The three legend tables (origin/value/goods) each carry a footnote — "If what you have is not listed, take the nearest entry above it" — which didn't apply here since all three inputs (Daejeon, 300M won, office consumables) matched an exact row, but it's worth flagging as a place where a less exact match in the question could require a judgment call. No other ambiguity in this walk.
