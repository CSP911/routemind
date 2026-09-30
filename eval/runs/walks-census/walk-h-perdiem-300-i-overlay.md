1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "MD, Tokyo, one night — hotel per-night cap and receipt threshold" --member /v1/regions/expense "trip expense, hotel allowance and receipt rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_1209b3 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body

2. **Answer**:
Lodging cap: 287 USD per night. Receipt threshold: 30 USD — spend above this amount requires a receipt to be kept as evidence.
(For reference, same row also gives meals 65 USD/day and incidentals 13 USD/day, but these weren't asked for.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions is current for a 2026-09-21 question)
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body (the row itself: lodging 287 USD/night, receipt threshold 30 USD)

4. **Notes**:
The overseas per-diem subject has three superseding versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) and the legend-revision page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01, and that the oldest version never says it was replaced. Today's date (2026-09-21) falls cleanly in the current table's range, so this wasn't actually a hard call here, but it would have been easy to skip that check and grab the first per-diem-looking row I saw. The table itself is indexed by three separate legends (grade, band, stay) rather than by plain-English terms like "managing director" or "Tokyo," so the job title and city had to be translated through those legend tables before the row address could even be constructed — none of those codes (G4/B1/S1) are guessable, they had to be read off the legends. No ambiguity in the mapping itself: MD → G4, Tokyo → B1, one night → S1 were all unambiguous exact matches, not nearest-entry fallbacks.
