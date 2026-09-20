1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m3/body

2. **Answer**:
For category C4, amount V4, term M3 (in force from 2026-01-01, current as of today 2026-09-20/21): the division director signs it off. Delegation limit is 100062 thousand KRW. Yes, other prices are required first: three competing quotes plus a written comparison. Working days to expect: 13.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies to today's date)
- /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m3/body (the answer)

4. **Notes**:
The procurement area warns up front that approval-threshold has THREE versions covering different date ranges, and that "the oldest says nothing at all about having been replaced" — so reaching for the current table without checking dates would be a mistake for older questions. I checked the legend-revision page to confirm 2026-09-20 falls in the "2026-01-01 onwards" range, which maps to `sec-hard-threshold`. That table conveniently listed a direct row per category/amount/term combination (indexed by three qualifiers), so I could jump straight to `hard-threshold-row-category-c4-amount-v4-term-m3` without needing to open the amount/category/term legend files at all — the question already gave the codes (C4, V4, M3) rather than plain-language values that would have needed translating. The only near-miss was almost skipping the version-date check and just grabbing the first "current" table that appeared in the procurement listing.
