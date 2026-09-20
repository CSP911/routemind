1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body

2. Answer
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Also on this row, for context: screening score required 57; financial statements for the last two years.)

3. Source
/v1/nodes/hard-diligence-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
/v1/nodes/sec-hard-diligence (current supplier due diligence table, in force from 2026-01-01)
/v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body (the answer)

4. Notes
Supplier due diligence exists in three versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that the oldest version says nothing about being superseded — reaching for it without checking dates would silently give a wrong, out-of-date answer. Today's date (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` was correct, but this is exactly the kind of question where grabbing the first/oldest-looking match would have been wrong. No other ambiguity: O2/W3/K4 exists as an exact row in the current table, so no legend interpretation (for origin/value/goods codes) was needed.
