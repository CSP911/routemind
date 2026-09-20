1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body

2. **Answer**
Lodging cap: 99 USD per night. Receipt required above: 21 USD (the receipt threshold).
(For context, same row also gives meals at 43 USD/day and incidentals at 8 USD/day, but the question only asked about lodging.)

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body (junior analyst → grade G1)
/v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
/v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body (the figures)

4. **Notes**
The expense area lists three per-diem documents: `hard-perdiem-legend-revision`, `hard-perdiem-v2` (marked SUPERSEDED, 2024-07-01 to 2025-12-31), and `sec-hard-perdiem` (marked as the current table, in force from 2026-01-01). It would be easy to grab `hard-perdiem-v2` by mistake since it sorts near the legend file and isn't obviously old until you read the label — I didn't open it, but the naming is a trap for a careless walk. Today's date (2026-09-20) falls inside the `sec-hard-perdiem` validity window, so that's the one I used.

The per-diem table itself doesn't spell out grade/band/stay in plain English — it's indexed by codes (G1/B1/S2 etc.), and each of the three legends says explicitly "this table is the only place the mapping is written down," so skipping any one of them would make the row address unguessable rather than just inconvenient. Nothing else about the walk was ambiguous — the row itself directly labels "Receipt threshold," so no inference was needed for the second half of the question.
