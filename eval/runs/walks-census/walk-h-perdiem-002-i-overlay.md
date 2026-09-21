1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Junior analyst, Tokyo, 8 nights: nightly hotel cap and receipt threshold?" --member /v1/regions/expense "trip lodging caps and receipt requirements live under expense"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_bea129 --outcome answered --used /v1/regions/expense /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 103 USD per night. Receipt has to be kept for any spend above 24 USD (the receipt threshold). This is from the current overseas per-diem table, in force from 2026-01-01 — junior analyst = grade G1, Tokyo = band B1, eight nights = stay S3.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → B1)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → S3)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body (103 USD lodging, 24 USD receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms current table applies for 2026 dates)

4. **Notes**:
The per-diem table is indexed by three separate qualifiers (grade, country band, stay length) each resolved through its own legend — none of the three is guessable from the question wording alone ("junior analyst," "Tokyo," "eight nights" each had to be looked up, not assumed). The table listing under /v1/nodes/sec-hard-perdiem flagged a versioning warning (hard-perdiem-legend-revision) noting three historical versions of this table exist, and that reaching for the newest is wrong for any question dated before 2026-01-01. Today's date (2026-09-21) is safely inside the current table's range, so no version confusion here — but this is exactly the kind of question where grabbing the first per-diem row found without checking the date would silently give the wrong figures for an older trip. Also worth flagging: the row's own text notes an "unavoidable excess" over the cap can still be claimed with a written statement and evidence, decided by the budget holder — not asked here, but adjacent and easy to conflate with the flat cap.
