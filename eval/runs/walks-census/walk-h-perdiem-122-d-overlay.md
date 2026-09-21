1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G2, band B3, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip hotel per diem and receipt retention threshold"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py overlay add --id ov_2026-09-21_f9430b --address /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body --why "the exact G2/B3/S3 row with nightly lodging cap and receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f9430b --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body

2. **Answer**: Lodging cap is 199 USD per night. The receipt has to be kept for any spend above 46 USD (the receipt threshold). (For context, the same row also gives 85 USD/day for meals and 17 USD/day for incidentals, but those weren't asked.)

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body

4. **Notes**: The expense area table lists two per-diem-looking nodes right next to each other — `hard-perdiem-legend-revision` (a warning that overseas per-diem has three versions with different dates) and `hard-perdiem-v2` (explicitly SUPERSEDED, covering 2024-07-01 to 2025-12-31). It would be easy to grab `hard-perdiem-v2` by mistake since it sorts right above the current table in the listing and looks authoritative at a glance. The actual current table is `sec-hard-perdiem`, in force from 2026-01-01, which the row body itself confirms is still current against today's date (2026-09-21) and explicitly names the superseded predecessors. No ambiguity once inside `sec-hard-perdiem`: the row addresses are literally named by grade/band/stay code, so G2/B3/S3 mapped directly to one file with no legend lookup needed.
