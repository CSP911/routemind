1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C3, amount V1, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - in force since 2026-01-01" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions with different dates - need to confirm current one applies"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_9aceef --outcome answered --used /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**: The team lead signs it off. No competing quotes are required ("Competing quotes: none"). Delegation limit is 1,032 thousand KRW, with 2 working days to expect. (This is the current table, in force from 2026-01-01, which applies to today's date of 2026-09-20/21.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed the current, three-qualifier table applies to today's date rather than the superseded v2 or oldest version)
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body (the actual figures: team lead, no quotes required)

4. **Notes**: Creating the overlay against /v1/nodes/sec-hard-threshold (the table listing) expanded it to every category/amount/term row in RouteMind, which is how the exact address for C3/V1/M1 surfaced — I never had to open the intermediate table separately. The one place this could have gone wrong is the version legend: the procurement table lists three separate threshold pages (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) and explicitly warns the oldest page never says it was superseded, so grabbing the first threshold-looking address without checking the date would have silently returned a stale answer. Checked the revision legend first and confirmed today's date falls under the current (2026-01-01 onwards) table before reading the row, so no wrong turn taken here.
