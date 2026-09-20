1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body

2. **Answer**: The department head signs it off. No competing quotes are required. (Delegation limit for this row is 1,034 thousand KRW; expect 4 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body

4. **Notes**: The three legends (category, amount, term) have to be resolved separately before the row address can be built — "flights and hotels" maps to category C3, "about 700,000 won" maps to amount V1, and "locked in for three years" maps to term M3, giving row c3-v1-m3. It would be easy to jump straight to a threshold row guessing at amount bands from real KRW figures, but the legend text is explicit that its mapping is the only place the correspondence is written and rows don't repeat it — so skipping the legends risks picking the wrong row even though the wording ("about 700,000 won") looks like it's already in the row's own language. Also worth flagging: the procurement table listing showed three historical versions of this threshold table (a legend-revision warning, a superseded 2024-07-01–2025-12-31 version `hard-threshold-v2`, and an older `threshold-table`). I used `sec-hard-threshold`, explicitly marked as in force from 2026-01-01, which covers today's date (2026-09-20/21), so the current table was the right one — but this is a spot where picking the superseded table by accident would give a wrong signer/quote answer without any obvious error.
