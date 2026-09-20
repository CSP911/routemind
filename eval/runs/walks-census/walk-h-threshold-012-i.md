1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body

2. **Answer**
Sign-off: the department head.
Quotes: yes, two competing quotes are required.
(Delegation limit for this row is 5006 thousand KRW, term is "locked in for three years" = M3, which covers this case.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body

4. **Notes**
The approval threshold subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 and that the oldest version says nothing about being replaced — an easy trap for a question dated in 2025. Today's date (2026-09-20) is safely within the current table's range (2026-01-01 onward), so `sec-hard-threshold` was correct, but I checked the revision page deliberately rather than assuming. The three qualifiers (category/amount/term) each had their own legend mapping plain-language descriptions to codes ("a couple of laptops" → C1, "roughly 3 million won" → V2, "locked in for three years" → M3); skipping any one of the three legends and guessing the code directly from the row list would have been easy to get wrong, since the row addresses only differentiate by code, not by the original wording.
