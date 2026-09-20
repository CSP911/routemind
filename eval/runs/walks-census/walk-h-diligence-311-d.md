1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body

2. **Answer**: No site visit is required. The file is re-reviewed every 24 months.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions applies to today's date)
- /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body (the answer: Site visit = no, Re-review interval = every 24 months)

4. **Notes**: Supplier due diligence has three superseded/current versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page explicitly warns that the oldest version never says it was replaced — so grabbing the first plausible-looking table without checking the revision legend would have silently given a wrong-era answer. Today (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` was correct, but this is exactly the kind of question where reaching for "the newest" without checking is only right by luck. The current table is indexed by three qualifiers (origin/value/goods) matching the question's O4/W2/K2 exactly, so once the right table version was confirmed, finding the row was unambiguous.
