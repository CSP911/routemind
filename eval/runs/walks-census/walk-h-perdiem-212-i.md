1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body

2. **Answer**:
Lodging cap: 247 USD per night. Receipt threshold: above 41 USD, a receipt must be kept.
(Grade G3 = department head, band B2 = Singapore, stay S3 = eight nights, current table in force from 2026-01-01.)

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/sec-hard-perdiem (table, for row index)
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body

4. **Notes**:
The area listing under /v1/regions/expense warns up front that overseas per-diem has three superseded/current versions and that the oldest one "says nothing at all about having been replaced" — reading the revision legend first before trusting the top-billed `sec-hard-perdiem` table was necessary, since blindly grabbing the newest-looking table could have been right here (today is 2026-09-20, so current does apply) but only by luck rather than by checking. Also worth flagging: "eight nights" maps exactly to stay S3 with no rounding or nearest-band judgment needed, unlike grade/band which required a one-to-one lookup from plain-language terms ("department head" → G3, "Singapore" → B2) via the legend tables — skipping those legends and guessing the codes would have been an easy mistake since the row addresses are not otherwise decodable from the question terms.
