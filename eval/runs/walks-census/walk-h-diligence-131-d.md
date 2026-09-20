1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body

4. **Notes**
The procurement table listed three versions of the supplier due diligence rules (a "legend-revision" warning, a superseded `hard-diligence-v2`, and the current `sec-hard-diligence`). It would have been easy to grab the wrong version — the current table's own footer confirms it's in force from 2026-01-01 with no end date, which covers today (2026-09-20), so I didn't need to open the legend-revision page separately. Row addresses are directly keyed by origin/value/goods code (e.g. `-origin-o2-value-w4-goods-k2-`), so once the target row's address was visible in the table listing, no legend lookups for O2/W4/K2 definitions were needed either.
