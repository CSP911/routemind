1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body

2. **Answer**
The department head signs it off, and yes — two competing quotes are required. This is for category C1 (a couple of laptops), amount V2 (roughly 3 million won), term M2 (renewing every year). Delegation limit for this row is 5,005 thousand KRW; working days to expect is 6.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (confirms which version applies for today's date, 2026-09-20)
- /v1/nodes/hard-threshold-legend-category/body
- /v1/nodes/hard-threshold-legend-amount/body
- /v1/nodes/hard-threshold-legend-term/body
- /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body (the answer itself)

4. **Notes**
The approval threshold subject has three superseded/current versions of the same table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns explicitly that the oldest version says nothing about being replaced — so grabbing the first "approval threshold" table found without checking dates would silently give a 2024-era answer. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-threshold`) was correct, but this was a real branch point, not a formality. The category/amount/term mapping is also not obvious from the question's wording alone — "a couple of laptops," "roughly 3 million won," and "renewing every year" are literally the example phrasings used in the three legend tables, which made we suspect the question was deliberately built to match a specific row (C1/V2/M2) rather than requiring interpretation. No ambiguity remained once the three legends were read.
