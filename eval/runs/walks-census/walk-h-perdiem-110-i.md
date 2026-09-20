1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: Lodging cap is 175 USD per night. The receipt threshold is 31 USD — above that amount, evidence (a receipt) must be kept/attached; below it, none is required.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body (the figures: 175 USD lodging, 31 USD receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms the current table, in force from 2026-01-01, is the right version for today's date, 2026-09-20)

4. **Notes**: The per-diem table has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the region table's own description warns the older band-only caps are "still here and superseded" — it would have been easy to land on the wrong one without checking the legend-revision page against today's date. The three qualifiers (grade, band, stay) each have their own legend table that must be read separately before the row address can be built — nothing in the question uses RouteMind's own vocabulary ("G2", "B2", "S1") directly, so skipping any one legend risks guessing the row address instead of reading it off a printed table. The row bundles lodging, meals, receipt threshold, and incidentals together; the question only asked about the hotel cap and the receipt threshold, so meals/incidentals were left out of the answer as not asked for.
