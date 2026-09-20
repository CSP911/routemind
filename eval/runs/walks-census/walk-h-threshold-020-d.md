1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body

2. **Answer**
Signature: the department head signs it off.
Other prices: yes — three competing quotes are required.
(Context from the same row: delegation limit 20,008 thousand KRW; 8 working days to expect.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed the current, 2026-01-01-onward table is the right version for today's date, 2026-09-20)
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body (the answer)

4. **Notes**
The procurement area's table listing flags up front that "approval threshold" has three superseded-but-undeleted versions, and the oldest one says nothing about being replaced — so grabbing the first threshold-looking page found would silently give a stale answer. Reading the legend-revision page first to confirm 2026-09-20 falls in the "2026-01-01 onwards / sec-hard-threshold / three qualifiers" band was the step that kept this from going wrong. Once inside sec-hard-threshold, the row address is built from the codes the question already gave (C1, V3, M1), so no legend lookup for category/amount/term meanings was needed — the row existed verbatim in the table listing.
