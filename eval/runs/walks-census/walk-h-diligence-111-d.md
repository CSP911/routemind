1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body

2. **Answer**: No, a site visit is not required. The file (re-review) is looked at every 24 months.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions applies for today's date, 2026-09-20)
- /v1/nodes/sec-hard-diligence (table listing, located the O2/W2/K2 row)
- /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body (source of the answer: Site visit = no, Re-review interval = every 24 months)

4. **Notes**: The procurement area flags up front that supplier due diligence has three superseded versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with different date ranges, and warns that the oldest page gives no indication it was ever replaced — so grabbing the first plausible-looking due-diligence page without checking the legend-revision note would have been a real risk of landing on stale rules. Today's date (2026-09-20) falls clearly in the current version's range (2026-01-01 onwards), so no ambiguity there, but the check was necessary rather than assumed. The O2/W2/K2 row was addressable directly once the current table's listing was opened, since row addresses are built from all three qualifiers exactly as given in the question.
