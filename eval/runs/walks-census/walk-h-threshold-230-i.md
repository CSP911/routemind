1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**: The department head signs it off. Yes — three competing quotes and a written comparison are required first. (Delegation limit for this row is 100,044 thousand KRW; expect 11 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body
/v1/nodes/hard-threshold-legend-revision/body (used to confirm the current table applies to today's date)

4. **Notes**: "Flights and hotels" maps directly to category C3 in the category legend, "about 40 million won" maps directly to amount V4, and "just the once" maps directly to term M1 — all exact matches, no nearest-entry guessing needed. The main risk here was the threshold table's three-version history: the legend-revision page warns that the oldest version "says nothing at all about having been replaced," so it would be easy to land on a stale row (`hard-threshold-v2` or `threshold-table`) without checking. I confirmed today's date (2026-09-20/21) falls in the 2026-01-01-onwards range, so `sec-hard-threshold` is correct. I did not need to consult the expense region at all, even though "business trip" spend might intuitively sound like an expense-report question — the actual question (whose signature, how many quotes) is a procurement/purchase-request concept, and the procurement region's table led straight to it.
