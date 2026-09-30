1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C2, amount V3, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - likely has C2/V3/M1 answer" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold table has 3 versions - need to confirm which applies to today 2026-09-21" --member /v1/nodes/purchase-request "quotes/other prices requirement before purchase"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_516e48 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body

2. **Answer**
Yes — three competing quotes are required. The department head signs it off (delegation limit 20,024 thousand KRW for this row; 8 working days to expect).

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed today's date, 2026-09-21, falls under the current table)
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body (the actual figures)

4. **Notes**
The near-miss here was version confusion: the procurement area table lists three separate threshold pages (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) and warns explicitly that the oldest one "says nothing at all about having been replaced," so grabbing the first threshold-looking hit without checking the legend-revision page would silently give an outdated answer. Today's date (2026-09-21) is safely inside the "2026-01-01 onwards" current version, so no ambiguity in this case, but the check was necessary rather than assumable. Once on the current table, the row address was a direct, unambiguous match to the three qualifiers given in the question (C2/V3/M1) — no interpretation needed there.
