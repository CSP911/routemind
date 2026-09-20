1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body

2. **Answer**: For category C3, amount V3, term M2 (current table, in force from 2026-01-01): the department head signs it off. Yes, other prices are required first — three competing quotes. (Delegation limit 20041 thousand KRW; 9 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (established which version applies for today's date, 2026-09-21)
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body (the answer)

4. **Notes**: The procurement table warns up front that approval threshold has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and that the oldest version doesn't mention being superseded — reaching for the wrong one would give a wrong answer with no warning sign in the document itself. Checked the revision-legend page before trusting `sec-hard-threshold` as current; today's date (2026-09-21) falls after 2026-01-01 so the current table is correct. The row address matched the question's codes (C3/V3/M2) exactly, so no legend lookup for category/amount/term definitions was needed — worth flagging that if the question had used plain-language values instead of the C/V/M codes, the legend files (`hard-threshold-legend-amount`, `-category`, `-term`) would have been required first to translate them.
