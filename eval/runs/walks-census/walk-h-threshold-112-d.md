1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body

2. **Answer**:
For category C2, amount V2, term M3 (current table, in force from 2026-01-01, which covers today's date of 2026-09-20/21): the department head signs it off. Yes, other prices are required first — two competing quotes are needed. (Delegation limit for this row is 5,022 thousand KRW; working days to expect is 7.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies to today's date)
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body (the answer: signer and quote requirement)

4. **Notes**:
The procurement area lists three versions of the approval threshold (oldest single-qualifier table, a 2024-07-01–2025-12-31 middle version, and the current 2026-01-01 version), and a warning explicitly says the oldest table "says nothing at all about having been replaced," so grabbing the newest-looking table without checking the legend-revision page first would have been an easy way to get a plausible but wrong (or right-by-luck) answer for a differently-dated question. Today's date clearly falls in the current version's range, so this case wasn't the tricky one — but the legend page flags that 2025-dated questions are the case where reaching for either extreme (oldest or current) is wrong. Also worth noting: the row was already indexed by all three qualifiers (category/amount/term) directly in the sec-hard-threshold table listing, so no separate legend lookups for C2/V2/M3 meanings were needed to find the row — only to confirm the row's content once opened.
