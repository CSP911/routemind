1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row, for context: screening score required 93; financial statements — last three years, audited.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body

4. **Notes**
The due-diligence subject has three versions with overlapping/non-obvious boundaries (`supplier-due-diligence` until 2024-07-01, `hard-diligence-v2` for 2024-07-01–2025-12-31, and `sec-hard-diligence` for 2026-01-01 onward), and the revision-legend page explicitly warns that reaching for the newest table is wrong for any question dated before 2026-01-01, and that the oldest version says nothing about being superseded — so skipping that check could silently produce a stale answer. Today's date (2026-09-20) falls cleanly in the current table's range, so no real ambiguity here, but it was worth confirming rather than assuming "current" was right. The O4/W4/K4 row itself was unambiguous once the qualifiers were identified — no need to consult the origin/value/goods legend pages since the question already gave the codes directly.
