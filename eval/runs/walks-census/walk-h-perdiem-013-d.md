1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s4/body

2. **Answer**: For grade G1, band B2, stay S4 (current table, in force from 2026-01-01): the hotel/lodging cap is **123 USD per night**. A receipt must be kept for any spend **above 36 USD** (the receipt threshold). For reference, meals are capped at 67 USD/day and incidentals at 13 USD/day.

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s4/body

4. **Notes**: The expense area's table listing flags that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem` effective 2026-01-01). It would have been easy to grab an old version's row by mistake — I confirmed `sec-hard-perdiem` is the one in force as of today's date (2026-09-20) before reading the row, and the row body itself restates the same effective date, so no ambiguity remained. The row address for G1/B2/S4 was printed exactly in the table listing, so no address construction was needed.
