1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body

2. **Answer**:
Lodging cap: 227 USD per night. Receipt required for any spend above 29 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body

4. **Notes**:
The expense area's table listing flagged a real hazard up front: overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem` in force from 2026-01-01). It would have been easy to grab a stale table by name-matching alone. Since today's date is 2026-09-20, the current table (`sec-hard-perdiem`) is the right one, and its row for G3/B1/S2 confirmed the same 2026-01-01 effective date, so there's no version mismatch. The question gave grade/band/stay already as codes (G3, B1, S2), so no need to consult the legend files to translate a job title or destination city into a code — went straight to the matching row. No ambiguity in the final read.
