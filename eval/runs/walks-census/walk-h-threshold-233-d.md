1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m4/body

2. **Answer**
For category C3, amount V4, term M4 (current table, in force 2026-01-01 onward): the CFO signs it off. Yes, other prices are required first — three competing quotes plus a written comparison. Delegation limit is 100,047 thousand KRW; expect 14 working days.

3. **Source**
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m4/body
(context used to confirm the right version: /v1/nodes/hard-threshold-legend-revision/body)

4. **Notes**
The procurement area lists three versions of the approval-threshold subject (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about having been superseded — so grabbing the first plausible-looking row without checking the revision legend would have been an easy mistake. Today's date (2026-09-21/2026-09-20) falls in the current version's range (2026-01-01 onward), so `sec-hard-threshold` was correct, but this was a real branch point rather than an obvious one. Once in the current table, the C3/V4/M4 row existed directly and matched the question's qualifiers exactly — no interpolation or nearest-match guessing was needed.
