1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Managing director, Jakarta, 4 nights: hotel per-night cap and receipt threshold" --member /v1/regions/expense "business trip lodging caps and receipt requirements live under expense"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8f6195 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body

2. **Answer**: Lodging cap is 323 USD per night. The receipt threshold is 51 USD — above that amount, a receipt must be kept (and attached as evidence); below it, none is required.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions is in force for a 2026-09-21 question)
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body (the row itself: lodging 323 USD/night, receipt threshold 51 USD)

4. **Notes**: The overseas per-diem subject has three superseded/current versions living at different addresses (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision page warns explicitly that "reaching for the newest is wrong for anything before 2026-01-01" and that the oldest version says nothing about being replaced. Today's date (2026-09-21) falls after 2026-01-01, so the current table (`sec-hard-perdiem`) applies — but this is exactly the kind of question where grabbing the first per-diem table found without checking the revision legend would have silently given the wrong figures for a slightly earlier-dated question. The three-qualifier row address also isn't something to guess — it has to be assembled from three separate legend lookups (grade, band, stay), each of which explicitly instructs "if what you have is not listed, take the nearest entry above it," so a title like "managing director" or a city like "Jakarta" not literally on the list would need a judgment call; here all three matched exactly. Note the receipt threshold (51 USD) answers "above what amount must I keep the receipt" directly — it is not a cap on anything, just the line above which evidence is required.
