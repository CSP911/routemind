1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s2/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
```

2. **Answer**
Junior analyst = grade G1, Singapore = band B2, four nights = stay S2. For this row (current table, in force since 2026-01-01):
- Lodging cap: **115 USD per night**
- Receipt required above: **30 USD** (the receipt threshold)
(For context, also in this row: meals 57 USD/day, incidentals 11 USD/day, though not asked.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → B2)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → S2)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s2/body (the figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms this table, not an older version, applies to a 2026-09-20 date)

4. **Notes**
The expense area's table listing flags up front that overseas per-diem "has THREE versions with different..." — easy to grab the wrong one if you jump straight to a row without checking the revision-legend page. Today's date (2026-09-20) falls after 2026-01-01, so `sec-hard-perdiem` (three qualifiers: grade/band/stay) is correct; the two older versions (`hard-perdiem-v2`, `overseas-rates`) are superseded but still present and would give wrong numbers for a query dated today. The three legends (grade, band, stay) each warn "this table is the only place the mapping is written down" and must be read separately before the row address can even be constructed — nothing else tells you that "junior analyst" is G1 or that Singapore is B2, not B1. Also worth flagging: the row itself bundles lodging, meals, incidentals, and the receipt threshold together, so "per night hotel cap" and "receipt threshold" both come from the same single row — no need to separately consult the evidence/corporate-card tables for this specific figure.
