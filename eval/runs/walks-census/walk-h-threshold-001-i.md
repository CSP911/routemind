1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body

2. **Answer**
The team lead signs it off. No competing quotes are needed. (Delegation limit for this row is 1001 thousand KRW; expect 3 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (established the current table applies for 2026-09-20)
/v1/nodes/hard-threshold-legend-category/body (a couple of laptops → category C1)
/v1/nodes/hard-threshold-legend-amount/body (about 700,000 won → amount V1)
/v1/nodes/hard-threshold-legend-term/body (renewing every year → term M2)
/v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body (final answer)

4. **Notes**
The procurement table lists both a superseded `hard-threshold-v2` row set and the current `sec-hard-threshold` table side by side with no obvious flag distinguishing them at a glance — the legend-revision page is what actually resolves which one applies for today's date (2026-01-01 onward means the current `sec-hard-threshold` table is correct here). It would have been easy to grab `hard-threshold-v2` by mistake since it appeared right next to the current table in the same listing. Also worth noting: the three qualifiers (category, amount, term) each have their own legend translating plain-language descriptions into codes, and none of the "what you have" phrases in the question map literally onto the row addresses — a literal string match on "laptop" or "700,000" would fail; you have to go through the legends to get the C1/V1/M2 codes first.
