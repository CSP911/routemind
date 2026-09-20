1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body
```

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which version is in force for today's date)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body (site visit and re-review interval figures)

4. **Notes**
Supplier due diligence has three superseded versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns that "the oldest says nothing at all about having been replaced" — reaching for the newest table without checking the date would coincidentally have been fine here since today (2026-09-20) falls in the current version's range (2026-01-01 onward), but I checked the revision legend explicitly rather than assuming, since that's exactly the trap the page describes.

The question gave the origin/value/goods qualifiers already coded as O4/W3/K4, so no legend lookup (goods/origin/value legends) was needed to translate plain-language qualifiers into codes — the row address was constructable directly from the table listing.

One oddity worth flagging: the row document's closing section ("If the figures are exceeded") talks about excess amounts, claims, and budget holders — language that reads like it belongs to an expense/threshold table, not supplier due diligence. It looks like boilerplate carried over from another document type and is irrelevant to the site-visit/re-review question, but it's a place a careless read could go wrong by treating it as part of the diligence answer.
