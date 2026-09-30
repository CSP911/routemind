1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G4, band B2, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of three versions with different dates, need to confirm which applies to today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_965bf1 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body

2. **Answer**:
Lodging cap: 303 USD per night. Receipt required above 39 USD (the receipt threshold).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem table versions is current for today's date)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body (the figures)

4. **Notes**:
The expense area table flags up front that overseas per-diem has three superseded/current versions covering different date ranges, and that the oldest version doesn't say it was replaced — so grabbing the first per-diem-looking row without checking dates would have been wrong. Checked the legend-revision page first: today (2026-09-21) falls in the "2026-01-01 onwards" range, so `sec-hard-perdiem` (three-qualifier table) is the right one, not `hard-perdiem-v2` or `overseas-rates`. The row itself bundles lodging, meals, receipt threshold, and incidentals together — the receipt threshold (39 USD) is a separate figure from the lodging cap (303 USD) and it would be easy to conflate them or miss the receipt-threshold line since the question phrased it awkwardly ("what can I put on a hotel" = lodging cap; "above what amount do I have to keep the receipt" = receipt threshold, a single value covering the whole row, not hotel-specific). No ambiguity remained once the correct table version and row were confirmed.
