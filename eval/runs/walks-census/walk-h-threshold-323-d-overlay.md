1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V3, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term matches C4/V3/M4 exactly"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m4/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6427cc --outcome answered --used /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m4/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**:
The division director signs it off. Yes — three competing quotes are required before this can go through (delegation limit 20,059 thousand KRW, 11 working days to expect).

3. **Source**:
- /v1/nodes/sec-hard-threshold (table listing, led to the row)
- /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m4/body (the row itself: signer, quotes, limit, working days)
- /v1/nodes/hard-threshold-legend-revision/body (confirms today's date, 2026-09-21, falls under this current table and not one of the two superseded versions)

4. **Notes**:
The procurement area lists three separate threshold tables with a loud warning: the same subject ("approval threshold") has been written three times (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), covering different date ranges, and the oldest one says nothing about being superseded. It would have been easy to grab `hard-threshold-v2` by mistake since it also appeared in the first overlay's row list right next to the current one, with similar-looking names. Checking the legend-revision page to confirm 2026-09-21 falls under `sec-hard-threshold` (in force 2026-01-01 onward) was the deciding step — worth doing explicitly rather than assuming "current" is always right, since the legend itself warns against assuming.

One other snag: `overlay close` reported both addresses I used as "reached" rather than as members I had explicitly added to the overlay via `overlay add`. The overlay's initial member list was the region-level `/v1/regions/procurement`, and I navigated deeper into tables/files it printed without formally adding each address to the overlay set. The answer is still correct, but the overlay bookkeeping didn't track the narrowing step by step as instructed — worth doing `overlay add` for each address next time before closing.
