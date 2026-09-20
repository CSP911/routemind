1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body

2. **Answer**
"A couple of laptops" = category C1; "around 12 million won" = amount V3 (delegation limit is 20,009 thousand KRW, i.e. ~20.009 million won); "renewing every year" = term M2. For this row (C1/V3/M2): the department head signs it off, and yes — three competing quotes are required before approval. Expect about 9 working days.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body

4. **Notes**
The table listing at /v1/regions/procurement flags up front that the approval-threshold subject has three superseded versions living side by side under similar names (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and none of the older ones say they've been replaced. It would be easy to grab the wrong one by pattern-matching on name alone. I deliberately read the legend-revision page first to confirm today's date (2026-09-20) falls in the "2026-01-01 onwards" band before touching any row data, rather than assuming the newest-looking table was correct.

The three qualifiers (category/amount/term) are each in their own legend file and the row address is built by concatenating the codes — none of this is stated as a formula anywhere, you have to infer the address pattern from the row listing in the sec-hard-threshold table. All three of "a couple of laptops," "around 12 million won," and "renewing every year" happened to match a legend row's wording exactly, so no fuzzy nearest-match judgment call was needed here — a cleaner case than the legends' own fallback instructions anticipate.
