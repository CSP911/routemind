1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B1, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip hotel per diem and receipt threshold likely live here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py overlay add --id ov_2026-09-21_4a855a --address /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body --why "exact row for G3/B1/S3 in the current per-diem table"
./bench/rmcli.py overlay add --id ov_2026-09-21_4a855a --address /v1/nodes/hard-perdiem-legend-revision/body --why "warns of three per-diem versions with different dates; must confirm which is current for 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4a855a --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: Lodging cap is 231 USD per night. A receipt must be kept for any spend above 32 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body

4. **Notes**: This domain has three overlapping versions of the overseas per-diem table (`overseas-rates` until 2024-07-01, `hard-perdiem-v2` from 2024-07-01 to 2025-12-31, and `sec-hard-perdiem` from 2026-01-01 onward), and the revision-legend page explicitly warns that grabbing the newest table is wrong for a question dated before 2026-01-01. Today's date (2026-09-21) falls cleanly in the current table's range, so this wasn't an ambiguous case in the end, but the near-miss would have been skipping that check and assuming "current" without confirming the date — the walk is deliberately set up so that habit gets punished on other dates. The question didn't say "overseas" explicitly, but "hotel per diem with receipt threshold" only exists under the overseas per-diem row structure (grade/band/stay), so the region pick was unambiguous once the table listing was seen.
