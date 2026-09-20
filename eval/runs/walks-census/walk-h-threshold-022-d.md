1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body

2. **Answer**
For category C1, amount V3, term M3 (delegation limit 20,010 thousand KRW), the division director signs it off. Yes — three competing quotes are required before approval (working days to expect: 10). This is the current table, in force from 2026-01-01 onwards, which applies to today's date (2026-09-20).

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version's date range applies)
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body (the answer itself)

4. **Notes**
The procurement area lists three versions of the approval-threshold subject (old, v2, current), all still present with no indication on the oldest that it was superseded — the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. It would have been easy to jump straight to `sec-hard-threshold` since it's labeled "current," but I checked the legend first to confirm today's date (2026-09-20) actually falls in its 2026-01-01-onwards range rather than assuming. Once at the table, the row for C1/V3/M3 existed exactly as a direct address (`hard-threshold-row-category-c1-amount-v3-term-m3`), so no further legend lookups (amount/category/term definitions) were needed since the question already gave the codes directly rather than plain-language descriptions.
