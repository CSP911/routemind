1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body
```

2. **Answer**
Lodging (hotel) cap: 287 USD per night. Receipt required above 30 USD (the receipt threshold).
(For reference, the same row also gives meals at 65 USD/day and incidentals at 13 USD/day, but the question only asked about hotel and receipt threshold.)

3. **Source**
- `/v1/nodes/hard-perdiem-legend-revision/body` (confirmed which of the three per-diem versions applies for today's date, 2026-09-20)
- `/v1/nodes/sec-hard-perdiem` (table listing, confirmed the G4/B1/S1 row exists directly — no legend lookup needed since grade/band/stay codes were given in the question)
- `/v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body` (the answer: lodging 287 USD/night, receipt threshold 30 USD)

4. **Notes**
The expense area's table listing explicitly warns that overseas per-diem "has THREE versions with different effective dates" and one older version "says nothing at all about having been replaced" — so grabbing the first-looking per-diem file without checking dates would have been an easy mistake. I read the legend-revision file first to confirm that for today's date (2026-09-20), the current table (`sec-hard-perdiem`, in force from 2026-01-01) is correct, not `hard-perdiem-v2` or `overseas-rates`. No ambiguity on the row itself: the question already gave grade/band/stay as G4/B1/S1, so no legend lookups (grade/band/stay legends) were needed — the row address could be built directly from the pattern shown in the table listing.
