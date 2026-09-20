1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body

2. Answer
No site visit is required. The file gets re-reviewed every 36 months. (Screening score required: 30; financial statements not required — not asked, but part of the same row.)

3. Source
/v1/nodes/hard-diligence-legend-revision/body (established which of three versions applies to today, 2026-09-20 → current table)
/v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
/v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
/v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body (the answer: site visit no, re-review every 36 months)

4. Notes
The near-miss here was version selection: the procurement table lists three superseded/current versions of the supplier due diligence subject (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that a 2025-dated question needs the middle version, not either extreme. Today's date (2026-09-20) is safely inside the current table's validity (2026-01-01 onward), so `sec-hard-diligence` was correct, but I made a point of reading the revision legend before touching any row data rather than assuming the top-listed/current table was right — the warning text makes clear that assumption is the trap being tested. The three-qualifier lookup (origin/value/goods) itself was mechanical once the three legend pages were read — each legend explicitly states "this table is the only place the mapping is written down," so guessing the code from the plain-English description instead of checking the legend would have been risky (e.g. it's not obvious without checking that "eight million won" is the lowest band W1 rather than some other cutoff-based tier).
