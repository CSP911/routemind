1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body

2. **Answer**
Signature: the CFO. Quotes: yes — three competing quotes plus a written comparison are required first. (Delegation limit for this row is 100,015 thousand KRW; working days to expect: 14.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body

4. **Notes**
The approval-threshold subject has three superseded versions on the same procurement area (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the revision-legend page explicitly warns that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-20/21) falls after the current table's 2026-01-01 start, so `sec-hard-threshold` was correct, but this was a real trap worth checking rather than assuming. All three qualifiers in the question — "a couple of laptops," "about 40 million won," and "until we cancel it" — happened to be verbatim phrases in their respective legends (category C1, amount V4, term M4), so no judgment calls or nearest-entry approximations were needed here. The only mild ambiguity was whether "a couple of laptops" (a hardware purchase) might instead belong under some other category not shown in the truncated table-list description ("how far up this amount has to be…"), but the category legend confirmed it directly.
