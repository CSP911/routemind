1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body

2. **Answer**: For grade G2, band B3, stay S1 (current table, in force from 2026-01-01): lodging cap is 191 USD per night. A receipt must be kept above 40 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date)
/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body (the figures)

4. **Notes**: The expense area flags up front that overseas per-diem has three superseded/current versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) and warns that the oldest version never says it was replaced — reaching for the newest without checking the date would be wrong for a question dated before 2026-01-01. Today's date (2026-09-20) falls under the current table, `sec-hard-perdiem`, so that was correct here, but it's the kind of thing that's easy to get wrong by assuming "current" always applies. The row for G2/B3/S1 existed directly in the table listing, so no legend lookup (grade/band/stay definitions) was needed since the question already gave the codes explicitly.
