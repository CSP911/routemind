1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body

2. **Answer**:
Lodging (hotel) cap: 347 USD per night.
Receipt required for any spend above 66 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body

4. **Notes**:
No real ambiguity here — the question already gave grade, band, and stay codes (G4/B4/S4) directly, so the row was a straight lookup off the per-diem table's listing, with no need to consult the grade/band/stay legend files. The one thing worth flagging: the expense region's table description warns that "the older band-only caps are still here and are superseded," and the table itself lists three per-diem versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`). It would be easy to grab a superseded row by accident if you didn't check dates. I confirmed `sec-hard-perdiem` is explicitly marked as in force from 2026-01-01 with no end date, and today (2026-09-20) falls inside that range, so it's the correct, current table.
