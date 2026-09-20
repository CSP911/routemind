1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body

2. **Answer**: No site visit is required. The file is re-reviewed every 36 months. (This applies to the current table, in force from 2026-01-01: Da Nang = origin O4, ₩8,000,000 = value W1, a licence = goods K4. Screening score required is 81; financial statements are not required.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions applies for today's date)
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → O4)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → W1)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → K4)
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body (site visit: no; re-review interval: every 36 months)

4. **Notes**: The procurement area's table listing flags up front that supplier due diligence has three superseded versions living side by side (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and none of the older ones say they've been replaced — it would have been easy to grab the first "supplier due diligence" hit and get a stale rule. The legend-revision page settled that: today (2026-09-20) falls in the "2026-01-01 onwards" band, so `sec-hard-diligence` is correct. Also worth flagging: the "where to start" overview page mentions "a fourth page covering the ongoing side... re-run rather than one-off," which sounds like it might hold the re-review cadence — but that turned out to be a distractor for this question, since the actual per-supplier re-review interval lives directly on the matched origin/value/goods row, not on that fourth page. I didn't need to open it once the row itself gave both answers (site visit and re-review interval) directly.
