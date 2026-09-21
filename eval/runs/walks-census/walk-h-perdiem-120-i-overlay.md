1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Team manager, Jakarta, one night: hotel cap per night, and above what amount is a receipt required?" --member /v1/regions/expense "expense table covers business trip amounts, hotel allowances, and receipt thresholds"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4a58b0 --outcome answered --used /v1/regions/expense /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body

2. **Answer**: Hotel (lodging) cap is 191 USD per night. A receipt is required above 40 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions applies to today's date)
/v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
/v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
/v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body (the figures: 191 USD lodging/night, 40 USD receipt threshold)

4. **Notes**: The overseas per-diem subject has three superseding versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the revision-legend page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01, and that the oldest version says nothing about having been replaced — so skipping that check would have silently picked the wrong table on a differently-dated question. Today's date (2026-09-20/21) falls cleanly in the current table's range, so no ambiguity here, but the walk deliberately forced that check before reading the row. The other near-miss: the row page lists lodging, meals, receipt threshold, and incidentals together, and it would be easy to read "the amount" loosely and report the wrong figure (e.g. meals or incidentals) instead of the two the question actually asked for (lodging cap and receipt threshold) — the row's field labels are unambiguous once read carefully, but the four numbers sitting side by side is a place to slow down.
