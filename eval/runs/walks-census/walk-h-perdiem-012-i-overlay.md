1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Junior analyst, Singapore, 8 nights: hotel cap per night, and receipt threshold above which a receipt must be kept?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade, destination band, and length of stay - likely has the hotel cap" --member /v1/nodes/evidence "evidence rules may state the receipt threshold amount"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s3/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2e7d95 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s3/body

2. **Answer**: Hotel (lodging) cap is 119 USD per night. The receipt threshold is 33 USD — above that amount a receipt must be kept. (Grade G1 = junior analyst, Band B2 = Singapore, Stay S3 = eight nights, table in force since 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → grade G1)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s3/body (lodging 119 USD/night, receipt threshold 33 USD)

4. **Notes**: The per-diem rows are keyed by three separate legend lookups (grade, band, stay-length) rather than by the raw inputs, and each legend explicitly warns "this table is the only place the mapping is written down" — easy to guess wrong (e.g. assuming grades run the other direction, or eyeballing "8 nights" into the wrong band) if you skip straight to the row. The overlay I created named the section-level addresses (/v1/nodes/sec-hard-perdiem, /v1/nodes/evidence), not the individual leaf files I actually read, so the close command reported all four as "reached" rather than as named overlay members — worth noting since it means the overlay's own bookkeeping didn't track the real path I took. The bigger near-miss: /v1/nodes/qualified-evidence's /v1/nodes/qualified-list/body also has an "amount above which a receipt/simple receipt won't do" table, but it's a KRW-denominated general evidence-qualification rule, unrelated to the USD per-diem receipt threshold that answers this specific business-trip question. It would be easy to grab the wrong number by pattern-matching on "receipt threshold" without checking the currency and context.
