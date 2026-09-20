1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body

2. **Answer**
Yes, a site visit to the supplier's premises is required. The file is re-reviewed every 6 months. (For completeness: screening score required is 91, and audited financial statements for the last three years are required.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which version is current for today's date)
/v1/nodes/sec-hard-diligence (table of rows, confirmed this is the current version in force from 2026-01-01)
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body (the answer)

4. **Notes**
The procurement region table advertised the due-diligence table as "current since 2026-01-01" without qualification, so it would have been easy to jump straight to `sec-hard-diligence` and read the O4/W4/K2 row without checking. But the region listing also flagged a `hard-diligence-legend-revision` file warning that the subject has THREE versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and that the oldest version says nothing about being superseded — a trap for anyone who finds the old page first via search rather than through the region table. Since today's date (2026-09-20) falls after 2026-01-01, the current table `sec-hard-diligence` is the correct one to use, which I confirmed before reading the row. Nothing else was ambiguous — the O4/W4/K2 row was listed explicitly and unambiguously in the table.
