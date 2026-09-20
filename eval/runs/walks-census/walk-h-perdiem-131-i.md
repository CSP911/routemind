1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s2/body

2. **Answer**: A team manager on a 4-night trip to Dhaka may put up to 211 USD per night on the hotel. A receipt is required above 52 USD.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s2/body (lodging cap 211 USD/night, receipt threshold 52 USD)

4. **Notes**: The overseas per-diem area has three superseded versions in play (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem` from 2026-01-01) — easy to grab the wrong one if you don't check the effective dates against today (2026-09-20), which land squarely in the current table's range. The three legends (grade, band, stay) are the only place the mapping from plain-English terms to row codes is written, and none of that mapping is repeated in the row table itself — skipping any one of them means guessing at the row address, which the tool warns against ("never build one"). The row bundles both the hotel/lodging cap and the receipt threshold together, so no separate lookup was needed for the receipt question once the right row was found.
