1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body
```

2. **Answer**
For grade G4, band B3, stay S2 (current overseas per-diem table, in force from 2026-01-01):
- Lodging (hotel), per night: 323 USD
- Receipt threshold: 51 USD — a receipt must be kept for any spend above this amount

(For context, the same row also lists meals at 98 USD/day and incidentals at 20 USD/day.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body

4. **Notes**
The grade/band/stay codes given in the question (G4, B3, S2) matched a row address exactly, so no detour through the grade/band/stay legends (`hard-perdiem-legend-grade`, `hard-perdiem-legend-band`, `hard-perdiem-legend-stay`) was needed. The one thing worth flagging: the expense area's table listing explicitly warns that overseas per-diem has three versions with different figures (current since 2026-01-01, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and an older `overseas-rates`). I deliberately opened `sec-hard-perdiem` (the one the region table marks as current) rather than the superseded nodes — easy to grab the wrong version's number if you don't read that warning line first.
