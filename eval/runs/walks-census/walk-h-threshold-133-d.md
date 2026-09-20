1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body

2. **Answer**
For category C2, amount V4, term M4 (current table, in force from 2026-01-01): signs it off — the CFO. Yes, other prices are required first — three competing quotes plus a written comparison. (Delegation limit is 100031 thousand KRW, working days to expect is 14.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed today's date, 2026-09-21/2026-09-20, falls under the current version, not the superseded ones)
/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body (the actual figures)

4. **Notes**
The procurement area lists three versions of the threshold table (oldest, a 2024-07-01–2025-12-31 middle version, and the current one from 2026-01-01), with an explicit warning that the oldest version says nothing about being superseded and could be mistaken for current if picked without checking dates. Reading the legend-revision page first before trusting `sec-hard-threshold` avoided that trap — today's date (2026-09-20/21) clearly falls after 2026-01-01 so the current table applies, but it would have been easy to just grab the first threshold-looking table found. The row address for C2/V4/M4 was printed directly in the table listing, so no legend lookups (amount/category/term definitions) were needed to map qualifiers to codes — the question already used the row's own code vocabulary.
