1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body

2. **Answer**:
Site visit: no. Re-review interval: every 24 months.
(For reference, the same row also lists: screening score required 53, financial statements from last year.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body (the answer)

4. **Notes**:
The procurement area warns up front that supplier due diligence has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and that "the oldest says nothing at all about having been replaced" — so grabbing the first due-diligence table found without checking dates would have silently given stale figures. Checked the legend-revision page first to confirm today's date (2026-09-20) falls under the current table `sec-hard-diligence`, then went straight there since it's indexed by exactly the three qualifiers (origin, value, goods) the question already supplied as codes — no need to consult the origin/value/goods legends since O2/W2/K4 were given directly rather than as plain-language descriptions. The row's "If the figures are exceeded" section is boilerplate about handling an exceeded threshold and isn't relevant to a site-visit/re-review question — ignored it.
