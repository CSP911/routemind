1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body
./bench/rmcli.py read /v1/nodes/sec-hard-perdiem/body

2. **Answer**:
Lodging cap per night: 331 USD.
Receipt required above: 57 USD (the receipt threshold).
(For context, not asked but on the same row: meals 108 USD/day, incidentals 22 USD/day.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body
/v1/nodes/sec-hard-perdiem/body (confirms "receipt threshold" is the per-spend amount above which a receipt is required)

4. **Notes**:
The expense region table warns up front that overseas per-diem has three versions in force at different times (an older band-only-cap version and a 2024-07-01–2025-12-31 version are both still present alongside the current one), so it would be easy to grab a superseded row by mistake. The current table is explicitly `sec-hard-perdiem` (in force from 2026-01-01), and since today's date is 2026-09-20 that's the correct one — I didn't need to touch `hard-perdiem-v2` or `overseas-rates` at all, but a careless walk could easily land on the wrong version since all three showed up in the same area listing. The question already supplied exact grade/band/stay codes (G4/B3/S4), so the row address could be assembled directly from the table listing without needing to consult the grade/band/stay legend files.
