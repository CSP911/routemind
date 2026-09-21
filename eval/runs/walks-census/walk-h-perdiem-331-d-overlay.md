1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G4, band B4, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per diem and receipt threshold are expense policy topics"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6c4601 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body

2. **Answer**: Lodging cap is 339 USD per night. A receipt must be kept for any spend above 60 USD (the receipt threshold). (For context, meals are 112 USD/day and incidentals 23 USD/day, but those weren't asked.)

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body

4. **Notes**: The expense area's overlay listed a warning up front — overseas per-diem has THREE versions in force at different date ranges (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-perdiem` table for 2026-01-01 onward). It would have been easy to grab the superseded `hard-perdiem-v2` node by mistake since it was sitting right there in the same working-set listing with an enticing name. Today's date (2026-09-21) falls inside the current table's effective range, and the row itself restates "In force from 2026-01-01," so I used that one and didn't need to open the legend-revision or v2 documents. The grade/band/stay codes in the question mapped directly to a row address (`hard-perdiem-row-grade-g4-band-b4-stay-s2`) without needing the legend files that translate job titles or destination cities into codes.
