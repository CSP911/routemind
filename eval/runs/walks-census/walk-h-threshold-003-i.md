1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/sec-hard-threshold/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**: The department head signs it off. No competing quotes are required. (Delegation limit for this row is 1,003 thousand KRW; expect 5 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body (mapped "a couple of laptops" → category C1)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "about 700,000 won" → amount V1)
- /v1/nodes/hard-threshold-legend-term/body (mapped "until we cancel it" → term M4)
- /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body (the answer: department head signs, no quotes needed)

4. **Notes**: All three legend mappings ("a couple of laptops", "about 700,000 won", "until we cancel it") were verbatim exact matches to legend table entries, so no interpretation or nearest-entry judgment was needed — that's a rare, clean case. The one place I nearly went wrong was the version: the procurement table listed three "hard-threshold" pages (a legend-revision warning, the superseded v2, and the current sec-hard-threshold), and I almost skipped the revision-legend check since the current table looked obviously right. I read it anyway and confirmed today's date (2026-09-20) falls in the "2026-01-01 onwards" current-version window, so the current table was in fact correct — but the warning explicitly calls out that reaching for the newest table without checking is wrong for older dates, so this check was worth doing rather than assuming.
