1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body

2. **Answer**: Lodging cap is 187 USD per night. The receipt threshold is 40 USD — spend above that amount requires a receipt to be kept as evidence.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established the 2026-01-01-onward table is the one in force for today's date)
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body (the figures: 187 USD/night lodging, 40 USD receipt threshold)

4. **Notes**: The per-diem subject has three superseding versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision page explicitly warns the oldest one never says it was replaced — so checking today's date (2026-09-20) against the revision table before picking a row was necessary; skipping that step could easily have landed on the wrong superseded table. The three qualifiers (grade, band, stay) each have their own legend file with no overlap in naming (G-codes, B-codes, S-codes), and "three weeks" mapped exactly onto "stay S4" so no nearest-match judgment call was needed there. One thing worth flagging to the reader: the table's figures are denominated in USD, not SGD, even though the destination is Singapore — nothing in the walk indicated a currency conversion is required, but it's easy to misread as a local-currency figure.
