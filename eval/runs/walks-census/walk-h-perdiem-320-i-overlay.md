1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Managing director, Jakarta, one night - hotel cap per night and receipt threshold" --member /v1/regions/expense "expense region covers business trip pay, hotel, and receipt rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_490ae2 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body

2. **Answer**: Hotel (lodging) cap is 319 USD per night. A receipt is required for any spend above 48 USD (the receipt threshold). For reference, the same row also gives meals at 93 USD/day and incidentals at 19 USD/day.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body

4. **Notes**: The overseas per-diem subject exists in three superseded-but-not-marked-superseded versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision page warns explicitly that reaching for the newest one is wrong for any date before 2026-01-01, with the oldest version giving no hint that it was ever replaced. Today's date (2026-09-21) falls after 2026-01-01, so the current table (`sec-hard-perdiem`) was correct here, but this is an easy place to get a stale answer without checking the date first — I deliberately read the revision-legend page before touching the table. The three qualifiers (grade/band/stay) also each needed their own legend lookup to convert "managing director" → G4, "Jakarta" → B3, "one night" → S1 before the row address could even be constructed from what the table printed; guessing at the row address would have been wrong since addresses must come from what a table prints, not be built by hand. One bookkeeping wrinkle: the overlay was created with only `/v1/regions/expense` as a member, and the leaf documents actually used were read directly from tables opened along the way rather than added as overlay members first — the close command accepted them but flagged them as "reached ... from somewhere the overlay never named."
