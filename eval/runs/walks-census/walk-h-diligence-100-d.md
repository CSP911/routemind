1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months. (For reference, the same row also requires a screening score of 46 and does not require financial statements.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirms which version is current for today's date)
/v1/nodes/sec-hard-diligence (table listing, to find the O2/W1/K1 row address)
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body (the answer)

4. **Notes**
Supplier due diligence has three superseding versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page explicitly warns that the oldest version says nothing about being replaced — reaching for it without checking dates would silently give a wrong, out-of-force answer. Today (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` is correct; I confirmed this via the legend page before reading the row rather than assuming "current" was right by name alone.

The row document ends with a boilerplate "If the figures are exceeded" section about unapproved excess and budget-holder approval — that paragraph reads like it was copied from an expense/spend-threshold document and has nothing to do with site visits or re-review intervals. It's easy to misread as part of the diligence answer; it isn't, and I ignored it.

The table listing conveniently prints one file address per exact (origin, value, goods) combination, so no legend lookups for O2/W1/K1 codes were actually needed to find the row — I only needed the legend-revision page to pick the right table version.
