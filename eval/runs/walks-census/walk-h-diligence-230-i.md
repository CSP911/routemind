1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row, not asked but adjacent: screening score required 74; financial statements last three years, audited.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body (final answer: site visit yes, re-review every 6 months)

4. **Notes**
The procurement table surfaces three due-diligence tables side by side (`hard-diligence-v2`, current `sec-hard-diligence`, plus the legend-revision page) with no date filtering — it would be easy to grab the wrong version if I picked the first-looking match instead of checking the legend-revision page first. That page explicitly warns the oldest version doesn't announce its own replacement, so skipping it and reading `supplier-due-diligence` directly would have silently given stale rules. Today's date (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` is correct.

The three qualifiers (origin/value/goods) are each in a separate legend file, not in the row list itself, and the row table lists 64 nearly-identical-looking addresses differing only by o/w/k suffix — easy to mistranscribe. I resolved each qualifier independently (Austin=O3, 700M won=W4, office consumables=K1) before constructing the row address, rather than guessing the pattern.
