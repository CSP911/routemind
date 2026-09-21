1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Stuttgart firm, 60M KRW contract, licence supplied - site visit required? review/renewal frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, likely has site-visit and review-frequency rules by origin/value/goods" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, may point to the right sub-page for site visits/reviews" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence rules with different dates - need to confirm which version applies today"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a94596 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body

2. **Answer**:
No, a site visit is not required. The file is re-reviewed every 24 months.
(Full row: screening score required 53, financial statements from last year, site visit no, re-review interval every 24 months.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body — established the current (2026-01-01 onward) table is the correct version for a 2026-09-20 question
- /v1/nodes/hard-diligence-legend-origin/body — "a firm in Stuttgart" maps exactly to origin O2
- /v1/nodes/hard-diligence-legend-value/body — "sixty million won" maps exactly to value W2
- /v1/nodes/hard-diligence-legend-goods/body — "a licence" maps exactly to goods K4
- /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body — the answering row (site visit: no; re-review interval: every 24 months)

4. **Notes**:
The three qualifiers (origin, value, goods) all happened to be exact, literal matches to the legend wording ("a firm in Stuttgart", "sixty million won", "a licence"), so there was no ambiguity in classification — unlike the legend's warning about nearest-entry fallback, which wasn't needed here. The real trap was the version legend: the current due-diligence table only took effect 2026-01-01, and there are two older versions (one ending 2024-07-01, one running through 2025-12-31) indexed by fewer qualifiers under different node names (`supplier-due-diligence`, `hard-diligence-v2`). Since the question is dated 2026-09-20 (today), the current three-qualifier table (`sec-hard-diligence` / `hard-diligence-row-origin-o2-value-w2-goods-k4`) is correct, but it would have been easy to grab the wrong version's row shape (e.g. a two-qualifier row from `hard-diligence-v2`) if the date check were skipped. Also worth flagging: I included `/v1/nodes/sec-hard-diligence` and `/v1/nodes/sec-supplier-due-diligence` as overlay members but never had to open them directly — the legends and the specific row answered everything, so the overlay's "reached" vs. "member" distinction shows those two were unnecessary scaffolding rather than dead ends.
