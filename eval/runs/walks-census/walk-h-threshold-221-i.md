1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body

2. **Answer**: The department head signs it. Yes — three competing quotes are required first. (Delegation limit for this row is 20,041 thousand KRW; working days to expect: 9.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body (mapped "flights and hotels" → category C3)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "around 12 million won" → amount V3)
- /v1/nodes/hard-threshold-legend-term/body (mapped "renewing every year" → term M2)
- /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body (the answer: department head, three quotes)

4. **Notes**: The procurement table lists three thresholds tables (`hard-threshold-v2`, superseded, and `sec-hard-threshold`/current) plus a "legend-revision" warning page saying there are THREE historical versions. I nearly went to check that revision-legend page, but the current table's own header already states it's in force "since 2026-01-01" and today is 2026-09-20, so the current table applies without needing the revision history — I skipped that page rather than open it needlessly. The bigger trap was the three legends: category, amount, and term each map plain-English phrasing to a code (C/V/M), and the row address has to be built by hand from those three codes exactly as printed (e.g. `hard-threshold-row-category-c3-amount-v3-term-m2`) — getting any one code wrong (e.g. reading "roughly 3 million" for V2 instead of "around 12 million" for V3) would silently return a valid-looking but wrong row, since every row has the same shape. "Around 12 million won" matched V3 exactly, so no rounding judgment call was needed there.
