1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C1, amount V1, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term, in force from 2026-01-01" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has THREE versions - need to confirm current one applies and check what C1/V1/M3 mean" --member /v1/nodes/purchase-request "how many quotes needed before purchase - relevant to 'other prices first'"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a42767 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body

2. **Answer**: The department head signs it off. No competing quotes are required (delegation limit 1002 thousand KRW, working days to expect: 4).

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed today's date, 2026-09-21, falls under the current three-qualifier table `sec-hard-threshold`, in force since 2026-01-01, rather than the superseded `hard-threshold-v2` or `threshold-table`)
- /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body (the actual answer: signer and quote requirement)

4. **Notes**: Opening the overlay for `sec-hard-threshold` auto-expanded into all 64 individual C×V×M row addresses (4 categories × 4 amounts × 4 terms), so the exact row for C1/V1/M3 was sitting right there rather than needing to be constructed — good thing, since the instructions forbid building an address by hand. The one place this walk could have gone wrong: there are three superseded versions of the threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page explicitly warns the oldest version doesn't announce that it's been replaced. Grabbing the first "approval threshold" looking table without checking dates would have risked landing on stale data — confirming today's date (2026-09-21) falls in the 2026-01-01-onward range for `sec-hard-threshold` was a necessary step, not a formality. The overlay's `purchase-request` member turned out unused — the row itself directly stated "Competing quotes: none," so there was no need to cross-check the general purchase-request quote rules.
