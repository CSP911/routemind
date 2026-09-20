1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s4/body
```

2. **Answer**
Lodging cap: 299 USD per night. Receipt threshold: 39 USD — a receipt must be kept for any spend above that amount.
(For context, also on this row: meals 80 USD/day, incidentals 16 USD/day.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s4/body

4. **Notes**
The expense area lists three versions of the overseas per-diem (a legend-revision warning, a superseded `hard-perdiem-v2`, and the current `sec-hard-perdiem`). The current table's own description states it took effect 2026-01-01 and is in force today (2026-09-20), so I used it directly and didn't need to open the legend-revision or v2 documents. The question already gave grade/band/stay as codes (G4, B1, S4) rather than descriptions, so the legend files (which map job titles/cities/trip lengths to those codes) weren't needed either — the row address matched exactly. Straightforward walk, no wrong turns.
