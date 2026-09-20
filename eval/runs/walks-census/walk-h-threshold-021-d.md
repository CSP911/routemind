1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body

2. **Answer**: For category C1, amount V3, term M2 (in force from 2026-01-01, current table): sign-off is by the department head. Yes — three competing quotes are required before approval. Delegation limit is 20009 thousand KRW, with 9 working days to expect.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
/v1/nodes/sec-hard-threshold (table listing confirming the row exists for these exact codes)
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body (the answer)

4. **Notes**: The procurement area warns of three historical versions of the approval threshold table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and current from 2026-01-01), and explicitly says reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls under the current table, so this wasn't a trap here, but it would have been easy to skip the version-check step and grab the wrong row for an older date. The question's codes (C1, V3, M2) matched the row-address naming scheme directly, so no legend lookups (amount/category/term) were needed to translate qualifiers into codes — I did not open those legend files since the codes were already given in the exact form the table indexes by.
