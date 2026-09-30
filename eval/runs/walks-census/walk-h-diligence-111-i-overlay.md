1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 60M, custom spec order: site visit required? Re-review frequency for their vendor file?" --member /v1/regions/procurement "procurement covers approval thresholds, vendor assessment, site visits, supplier requalification"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_8dd98d --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body

2. **Answer**
No, a site visit is not required. The vendor file (screening) is re-reviewed every 24 months.
(Full row: screening score required 51, financial statements from last year, site visit: no, re-review interval: every 24 months.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established which version is in force for today's date, 2026-09-21)
- /v1/nodes/hard-diligence-legend-origin/body (mapped "a firm in Stuttgart" → origin O2)
- /v1/nodes/hard-diligence-legend-value/body (mapped "sixty million won" → value W2)
- /v1/nodes/hard-diligence-legend-goods/body (mapped "something made to our spec" → goods K2)
- /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body (the answering row: site visit no, re-review every 24 months)

4. **Notes**
There are three versions of the supplier due diligence subject, and the legend-revision page is explicit that reaching for the newest table is wrong for any question dated before 2026-01-01 — a 2025-dated question would need `hard-diligence-v2` instead of the current `sec-hard-diligence`. Today's date (2026-09-21) falls after the current version's 2026-01-01 start, so `sec-hard-diligence` was correct here, but this is an easy trap to fall into on a similarly-worded question set earlier in the year — I checked the revision page before touching the row table specifically to avoid that.

All three qualifiers (origin, value, goods) matched an exact wording in their respective legends — "a firm in Stuttgart", "sixty million won", "something made to our spec" — so there was no ambiguity requiring the "nearest entry above it" fallback each legend describes. No real confusion on this walk; the only thing worth flagging is the version-date trap above.
