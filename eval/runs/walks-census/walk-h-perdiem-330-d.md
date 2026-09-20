1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s1/body

2. **Answer**
Lodging cap: 335 USD per night. Receipt required for any spend above 57 USD (the receipt threshold).

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s1/body

4. **Notes**
The expense area's table listing flags a landmine up front: overseas per-diem has three superseding versions (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-perdiem` from 2026-01-01). It would have been easy to grab a row from the wrong version. Since today is 2026-09-20, `sec-hard-perdiem` is the correct, currently-in-force table, and I didn't need to open the superseded ones. The G4/B4/S1 combination was given directly in the question, so no legend lookups (grade/band/stay) were needed — I went straight to the matching row address in the table listing rather than constructing it. The row bundles lodging, meals, receipt threshold, and incidentals together, so it's worth being precise that the question only asked about two of those four figures.
