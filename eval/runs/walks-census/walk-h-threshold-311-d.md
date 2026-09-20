1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**
For category C4, amount V2, term M2 (delegation limit 5,053 thousand KRW): the department head signs it off, and yes — two competing quotes are required before approval. Working days to expect: 6.

3. **Source**
/v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body
/v1/nodes/hard-threshold-legend-revision/body (used to confirm the current table, in force from 2026-01-01, is the correct version for today's date 2026-09-21)

4. **Notes**
The procurement table listing flagged upfront that the approval threshold subject "has THREE versions" and pointed to a legend-revision page — that warning stopped me from just grabbing `sec-hard-threshold` on faith. I checked the revision legend after reading the row, and it confirmed the current table (three-qualifier index, in force 2026-01-01 onward) is correct for today's date; the older `hard-threshold-v2` (2024-07-01 to 2025-12-31) and `threshold-table` versions would have been wrong. The revision legend explicitly warns that "the oldest says nothing at all about having been replaced," so if I'd stumbled onto `threshold-table` or `hard-threshold-v2` first without checking dates, I could easily have reported a stale signer/quote requirement. The row itself was unambiguous once found — C4/V2/M2 maps to exactly one file among the 64 rows in the current table, no interpretation needed.
