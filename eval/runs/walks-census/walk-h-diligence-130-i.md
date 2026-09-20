1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row, not asked but relevant context: screening score required 58; financial statements — last three years, audited.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body (Site visit: yes; Re-review interval: every 6 months)

4. **Notes**
The procurement area lists three parallel versions of the supplier due diligence rules (a legend-revision file, a superseded `hard-diligence-v2`, and the current `sec-hard-diligence`), which could easily lead to reading the wrong one. I went straight for `sec-hard-diligence`, whose table header states it is "in force from 2026-01-01" — since today is 2026-09-20, that's current, so no need to open the legend-revision page to arbitrate. Worth flagging that I took that shortcut rather than confirming via the revision-legend page directly.

Also, `sec-supplier-due-diligence` (the "where to start" overview) mentions a "fourth page covering the ongoing side of the same checks, re-run rather than one-off" without naming it outright — I initially thought that was where the re-review cadence would live. It turned out the specific row itself (origin/value/goods combination) already carries a "Re-review interval" field directly, so that overview page wasn't actually needed to answer this question. Didn't chase the fourth page further since the row answered both parts of the question directly.

The three-axis lookup (origin/value/goods → row) worked cleanly once the three legend pages were read; each legend explicitly says "take the nearest entry above it" if the given figure isn't listed exactly, but here all three inputs (Stuttgart, 700 million won, office consumables) matched a legend row exactly, so no interpolation was needed.
