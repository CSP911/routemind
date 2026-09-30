1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "I'm a managing director — Jakarta, eight nights — what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade, destination band, and length of stay — should give the hotel cap for MD/Jakarta/8 nights" --member /v1/nodes/hard-perdiem-legend-revision/body "warns there are three versions of the per-diem table with different dates — need to confirm which is current" --member /v1/nodes/evidence "what has to be attached as evidence for a spend — likely has the receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_2855a3 --address /v1/nodes/evidence --why "the per-diem row itself states its own receipt threshold (54 USD); no need for the general evidence table"
./bench/rmcli.py overlay close --id ov_2026-09-21_2855a3 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body /v1/nodes/hard-perdiem-legend-revision/body
```

2. **Answer**
Lodging (hotel) cap: 327 USD per night.
Receipt threshold: 54 USD — any spend above this amount requires a kept receipt.
(For reference, this row also carries meals at 103 USD/day and incidentals at 21 USD/day, though not asked.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body — mapped "managing director" → grade G4
- /v1/nodes/hard-perdiem-legend-band/body — mapped "Jakarta" → band B3
- /v1/nodes/hard-perdiem-legend-stay/body — mapped "eight nights" → stay S3
- /v1/nodes/hard-perdiem-legend-revision/body — confirmed the current table (2026-01-01 onward) applies to today's date, 2026-09-21
- /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body — the actual figures (327 USD lodging, 54 USD receipt threshold)

4. **Notes**
The per-diem table is indexed by three separate codes (grade, band, stay) that each have their own legend/lookup document — none of this is derivable without reading all three legends first, so the walk necessarily took four hops before reaching the actual figures. The trap to watch for is the revision-legend warning: it explicitly calls out that reaching for the newest table is wrong for dates before 2026-01-01, and that a 2025-dated question needs the *middle* version (`hard-perdiem-v2`), not the current one. Today's date (2026-09-21) is safely inside the current table's range, so no ambiguity applied here, but this is clearly the deliberate trap for this document family — it was worth the explicit check rather than assuming "current" was right by default. Separately, I pulled the general `/v1/nodes/evidence` table into the working set expecting the receipt threshold to live there, but it turned out to be inside the per-diem row itself; removed it from the overlay as unused before closing rather than leave a stale member.
