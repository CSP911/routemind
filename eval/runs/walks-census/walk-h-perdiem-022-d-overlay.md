1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B3, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "expense region covers business trip hotel per diem and receipt requirements"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_102e98 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body

2. **Answer**: Lodging cap of 135 USD per night; receipts must be kept above 42 USD.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to a 2026-09-21 question)
- /v1/nodes/sec-hard-perdiem (the current table, indexed by grade/band/stay, located the exact row)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body (the figures: 135 USD lodging/night, 42 USD receipt threshold)

4. **Notes**: The overseas per-diem subject has three versions in force over different date ranges, and the oldest one (`overseas-rates`) says nothing about having been superseded — so blindly grabbing the first per-diem-looking table would have risked citing outdated figures without any warning sign in the document itself. Checking `hard-perdiem-legend-revision` first to confirm 2026-09-21 falls under the current table (`sec-hard-perdiem`, in force from 2026-01-01) was the right caution before trusting the numbers. Once on the current table, the grade/band/stay row was an exact, unambiguous match — no need to consult the legend files for grade/band/stay definitions since the codes were given directly in the question.
