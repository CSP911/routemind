1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s3/body

2. **Answer**: Lodging cap is 119 USD per night. A receipt must be kept for any spend above 33 USD (the receipt threshold). (For context, this row also gives meals at 62 USD/day and incidentals at 12 USD/day, though those weren't asked.) This is the current per-diem table, in force from 2026-01-01.

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s3/body

4. **Notes**: A junior analyst maps to grade G1, Singapore maps to band B2, and eight nights maps to stay S3 — each mapping lives in its own legend file and none of it is guessable from the row addresses themselves, so all three had to be read before the right row (grade-g1-band-b2-stay-s3) could be picked out of the 64-row grid. The expense table's warning about three per-diem versions (current, `hard-perdiem-v2`, and `overseas-rates`) was a real trap: it would be easy to grab the first per-diem-looking node without checking which one is in force. `sec-hard-perdiem` is explicitly the current table (2026-01-01 onward), so that's the one used. The row itself states the receipt threshold directly, so no separate trip to the general `/v1/nodes/evidence` table was needed for this question.
