1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s3/body

2. **Answer**: Lodging cap is 119 USD per night. The receipt threshold is 33 USD — above that amount a receipt must be kept.

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s3/body (via /v1/nodes/sec-hard-perdiem and /v1/nodes/hard-perdiem-legend-revision, which confirmed this table version applies for a 2026-09-20 question).

4. **Notes**: The expense region flags that overseas per-diem has three versions of this table (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and warns that reaching for the newest is wrong for dates before 2026-01-01 — the near-miss here would have been to skip the legend and just grab whichever per-diem table looked current without checking the in-force date. Since today is 2026-09-20, `sec-hard-perdiem` (in force from 2026-01-01) is correct, but the check was necessary rather than assumed. The row for G1/B2/S3 existed directly and needed no interpolation.
