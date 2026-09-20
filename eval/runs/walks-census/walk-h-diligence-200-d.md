1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body

2. **Answer**
No, a site visit is not required for origin O3, value W1, goods K1. The file is re-reviewed every 36 months. (Screening score required: 62; financial statements: not required.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions is in force for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body (the answer)

4. **Notes**
The procurement table listed three due-diligence documents side by side (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no obvious indication from the row question alone which one is current — it would have been easy to grab the first plausible-looking row table without checking the legend-revision page first. That page confirms today's date (2026-09-20) falls under the current table `sec-hard-diligence` (in force 2026-01-01 onward), so this walk used the right version, but the trap is real: picking `hard-diligence-v2` instead (correct only for 2024-07-01–2025-12-31) would have given a different, wrong answer for the same O3/W1/K1 coordinates. The row itself also carries a boilerplate "If the figures are exceeded" section about budget/excess handling that reads like it belongs to an expense or spending-limit page, not a site-visit/re-review policy — it was ignored as irrelevant to this question, but it's worth flagging as a possible template artifact in the source data.
