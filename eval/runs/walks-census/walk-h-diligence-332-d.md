1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body

2. **Answer**
Yes, a site visit is required. The file (re-review) is looked at again every 6 months.
(For context: screening score required is 92, and audited financial statements for the last three years are required.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body

4. **Notes**
The procurement table warned that supplier due diligence has three versions (current, a 2024-07-01–2025-12-31 version `hard-diligence-v2`, and an older `supplier-due-diligence`), which could easily lead to reading the wrong row. I went straight to `sec-hard-diligence`, which is explicitly labeled as the table in force from 2026-01-01, and today's date (2026-09-20) falls inside that period, so no version-legend lookup was needed. The O4/W4/K3 combination was given directly in the question as codes rather than plain-language descriptions, so I did not need to consult the origin/value/goods legend files to translate anything — I went straight to the matching row address. The only place I could have gone wrong was picking a superseded table (`hard-diligence-v2` or the legend-revision page) instead of the current one; the region table's row descriptions made the current one unambiguous.
