1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C3, amount V4, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term is in the procurement region"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_502989 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body

2. **Answer**: For category C3, amount V4, term M1 (delegation limit 100,044 thousand KRW), the department head signs it off. Yes, other prices are required first: three competing quotes and a written comparison.

3. **Source**: /v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies), /v1/nodes/sec-hard-threshold (current table, in force 2026-01-01 onward), /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body (the row with the actual figures).

4. **Notes**: The approval threshold subject has three versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being superseded. Since today is 2026-09-21, the current table (`sec-hard-threshold`) was correct — but this was an easy place to get wrong by skipping the version check and just grabbing the first "approval threshold" table that came up in the overlay (`hard-threshold-v2` was listed right alongside it, unqualified, and would have given a wrong answer). The row address itself was directly guessable from the pattern (category-c3-amount-v4-term-m1), but I still opened the table listing rather than constructing the address, per the walk rules. When closing the overlay, all three addresses I used came back marked "reached" rather than as recognized members — I had read them directly instead of first adding them via `overlay add`, so the overlay never had them registered as members even though they were exactly the anticipated procurement-region path.
