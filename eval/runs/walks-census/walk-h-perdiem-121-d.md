1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body

2. **Answer**:
Lodging (hotel) cap: 195 USD per night.
Receipt threshold: 43 USD — above this amount a receipt must be kept.
(For context, same row also gives: meals 80 USD/day, incidentals 16 USD/day.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions is current for today's date, 2026-09-20)
- /v1/nodes/sec-hard-perdiem (table listing all grade/band/stay rows; located the exact row)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body (the answer)

4. **Notes**:
The expense region table flags up front that overseas per-diem has three superseded/non-superseded versions covering different date ranges, with a specific warning that the oldest version never says it was replaced — so grabbing the first per-diem-looking node without checking dates would have been a trap. Reading hard-perdiem-legend-revision first confirmed that since today (2026-09-20) falls in the 2026-01-01-onwards range, `sec-hard-perdiem` (three qualifiers: grade, band, stay) is the right table, not `hard-perdiem-v2` or `overseas-rates`. Once in `sec-hard-perdiem`, the row for G2/B3/S2 was directly addressed and required no further legend lookups since the grade/band/stay codes were already given in the question. No ambiguity beyond the version check.
