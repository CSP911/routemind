1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body

2. **Answer**:
Lodging cap: 143 USD per night. Receipt threshold: 45 USD — spend above this amount requires keeping the receipt.
(For context, the same row also gives Meals: 80 USD/day and Incidentals: 16 USD/day.)

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions is in force for today's date, 2026-09-20)
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body (the figures)

4. **Notes**:
The expense region table flags up front that overseas per-diem has three superseded/current versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) and warns that reaching for the newest without checking the date is wrong. It was worth reading the legend-revision doc before trusting `sec-hard-perdiem` — since today (2026-09-20) falls after 2026-01-01, the current table is correct, but this is exactly the kind of question where grabbing the current table on reflex could accidentally be right for the wrong reason on a differently-dated question. No ambiguity in locating the specific G1/B4/S1 row — the table listed all 64 grade/band/stay combinations directly, and the target row's address was unambiguous.
