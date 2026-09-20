1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body
```

2. **Answer**
Lodging cap: 111 USD per night. Receipts are required for any spend above 27 USD (the receipt threshold). This is from the current overseas per-diem table, in force since 2026-01-01, for grade G1 (junior analyst), band B2 (Singapore), stay S1 (one night).

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → B2)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → S1)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body (the figures: 111 USD lodging, 27 USD receipt threshold)

4. **Notes**
The expense area's table listing flagged that overseas per-diem has three versions in force at different times (`sec-hard-perdiem` current since 2026-01-01, `hard-perdiem-v2` superseded 2024-07-01–2025-12-31, and an older `overseas-rates`). It would have been easy to grab a superseded table by mistake — the row body itself restates "In force from 2026-01-01," which matches today's date (2026-09-20), so I trusted `sec-hard-perdiem` rather than second-guessing further. The three legends (grade/band/stay) had to be resolved separately before the row address could be built — the row addresses are not guessable from the question text alone (e.g. "Singapore" only becomes "b2" via the band legend), so all three lookups were necessary, not optional. No ambiguity in the mappings themselves: junior analyst, Singapore, and one night each matched an exact row in their respective legends, not a "nearest entry" fallback.
