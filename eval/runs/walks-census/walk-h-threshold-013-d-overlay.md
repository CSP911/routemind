1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V2, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold table is by category, amount, and term - matches question directly"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_99ca85 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body

2. **Answer**: The division director signs it off, and yes — two competing quotes are required before this can go through. (Delegation limit for this row is 5007 thousand KRW; 8 working days to expect. In force from 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three approval-threshold versions applies to today's date)
- /v1/nodes/sec-hard-threshold (opened the current table to find the exact row for C1/V2/M4)
- /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body (the row itself — signer and quote count)

4. **Notes**: The approval threshold subject has three versions in force over different date ranges, and a legend-revision page warns explicitly that reaching for the newest version is wrong for any question dated before 2026-01-01, and that the oldest version says nothing about having been replaced — so skipping that check could silently give you the wrong signer. Today's date (2026-09-21) falls inside the current version's range (2026-01-01 onwards), so `sec-hard-threshold` was correct here, but I read the revision-legend page first specifically to confirm that rather than assume it. The current table's index page lists every row explicitly by category/amount/term codes (C1/C2/C3/C4 × V1-V4 × M1-M4), so once the version was confirmed, finding the exact row for C1/V2/M4 was a direct lookup with no ambiguity. The overlay close reported the three addresses as "reached" rather than "used," because I never called `overlay add` to formally register them as members after the initial `create` — I read them by address directly off the tables. The outcome was recorded correctly regardless, but a stricter walk would add each address to the overlay as it's opened rather than relying on direct reads.
