1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body
```

2. **Answer**
Nightly hotel (lodging) cap: **199 USD per night**.
Receipt is required above **46 USD** (the receipt threshold given in the same row).
(For reference, the same row also gives meals at 85 USD/day and incidentals at 17 USD/day, though these weren't asked for.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (established which of three per-diem versions applies to today's date)
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body (the figures)

4. **Notes**
The one place this could easily go wrong is the per-diem versioning: the expense table lists three separate documents for overseas per-diem (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision doc warns explicitly that "the oldest says nothing at all about having been replaced" — so grabbing the first per-diem-looking row without checking the date would have silently pulled a stale rate. Today (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-perdiem`) was the correct one, but the check was necessary rather than assumed. The three legends (grade/band/stay) each state they are "the only place the mapping is written down," so skipping any one of them and guessing the row address directly would have been guessing an address rather than following one — the instructions require using printed addresses only, and the row address itself is only derivable by composing all three legend lookups. No other ambiguity: "team manager," "Jakarta," and "eight nights" mapped cleanly to exact rows in each legend with no nearest-neighbor judgment needed.
