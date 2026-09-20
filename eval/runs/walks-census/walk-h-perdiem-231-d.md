1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body
```

2. **Answer**
For grade G3, band B4, stay S2 (current table, in force from 2026-01-01):
- Lodging, per night: 275 USD
- Receipt threshold: 56 USD (above this amount a receipt must be kept)

(For context, the same row also lists Meals per day: 103 USD, and Incidentals per day: 21 USD, but those weren't asked for.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body (the figures)

4. **Notes**
The expense area lists three separate documents for overseas per-diem (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), and the older ones don't announce that they've been superseded. The legend-revision document was the only thing that made it safe to pick `sec-hard-perdiem` instead of the newer-looking-but-wrong `hard-perdiem-v2` (which covers 2024-07-01 to 2025-12-31, not today's date of 2026-09-20). Skipping that check would have been the easy way to go wrong here. Once on the current table, the row address was a direct, exact match for grade/band/stay — no ambiguity there.
