1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body

2. Answer: 35 — the checks-required figure for origin O2 at contract value W2, under the supplier due diligence version in force from 2024-07-01 to 2025-12-31.

3. Source: /v1/nodes/hard-diligence-legend-revision/body (to establish which version covers 2024-07-03), /v1/nodes/hard-diligence-v2/body (the O2×W2 table cell = 35).

4. Notes: The "first change" in the question is the 2024-07-01 cutover from the oldest (no-qualifier) supplier due diligence page to the two-qualifier `hard-diligence-v2` page — the legend-revision page names that date explicitly, so "two days after" lands squarely inside the v2 window (2024-07-01 to 2025-12-31), not on a boundary that could be misread either way.

The near-miss: `/v1/regions/procurement` also surfaces `sec-hard-diligence`, described as "THE CURRENT SUPPLIER DUE DILIGENCE TABLE" with a much bigger, three-qualifier (origin × value × goods) row structure and individual per-row file addresses. It's tempting to grab that one since it's the most prominent/detailed table in the listing, but it's only in force from 2026-01-01 onward — using it for a 2024 date would be wrong on both the qualifier count and the underlying figures. The legend-revision page was the only thing that made the version boundaries unambiguous.

Also worth flagging: the v2 table's cells are bare integers (30–45) with no in-page legend explaining what the numbers represent beyond "the checks required, by origin and value" — I took the cell value itself as the answer since the page states directly that this column *is* the checks-required figure, and confirmed no separate numeric legend exists elsewhere (checked `supplier-due-diligence/body` and `sec-supplier-due-diligence/body`, neither defines a numbered check scheme).
