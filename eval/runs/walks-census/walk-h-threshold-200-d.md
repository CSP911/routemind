1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body

2. **Answer**:
For category C3, amount V1, term M1: the team lead signs it off. No, you do not have to get other prices first — competing quotes required: none. (Delegation limit for this row is 1,032 thousand KRW; working days to expect: 2.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed today's date, 2026-09-21, falls under the current table, not the two superseded versions)
- /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body (the answer itself)

4. **Notes**:
The procurement area's table listing flagged that the approval-threshold subject has three versions covering different date ranges, with an explicit warning that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about having been replaced (so a naive walk could land on stale rules without any signal). I checked the legend-revision page before trusting `sec-hard-threshold`, which confirmed today's date (2026-09-21) sits in the "2026-01-01 onwards" current-version band, so no correction was needed. The category/amount/term qualifiers in the question (C3, V1, M1) mapped directly to one exact row address in the current table's listing, so no legend lookups for amount/category/term codes were needed — the row itself stated everything required, including the competing-quotes requirement.
