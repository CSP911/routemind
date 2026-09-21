1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G4, band B4, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip hotel per diem and receipt threshold likely live here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py overlay add --id ov_2026-09-21_d5efd8 --address /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body --why "exact row for grade G4, band B4, stay S3"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d5efd8 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body

2. **Answer**: Lodging cap is 343 USD per night. The receipt threshold is 63 USD — spend above that amount requires a receipt to be kept.

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body

4. **Notes**: The table at /v1/nodes/sec-hard-perdiem is explicitly flagged as "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01," and the row itself repeats that in-force date. Today is 2026-09-21, so this version applies cleanly — no need to touch the two superseded versions (`hard-perdiem-v2`, `overseas-rates`) noted in `hard-perdiem-legend-revision`. The question gave grade/band/stay codes directly (G4/B4/S3), so the legend files for translating job title → grade, city → band, and trip length → stay were not needed — I went straight to the row named for that exact combination. The only thing to watch here is the version trap flagged by `hard-perdiem-legend-revision`: if the question had involved a past date, picking the current table without checking the revision legend would have been the wrong move.
