1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body

2. **Answer**
For category C1, amount V2, term M3: signs off is the department head. Yes, other prices are required first — two competing quotes are needed. (Delegation limit for this row: 5,006 thousand KRW; working days to expect: 7.)

3. **Source**
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body

4. **Notes**
The procurement table warned that the approval-threshold rules have THREE versions (a "hard-threshold-legend-revision" doc flags this explicitly), so it would have been easy to grab a superseded table (`hard-threshold-v2`, in force 2024-07-01 to 2025-12-31, or the older `threshold-table`). The current table, `sec-hard-threshold`, states it has been in force since 2026-01-01, and today's date (2026-09-20) falls within that window, so I used it without needing to open the revision-legend doc. Because the question gave the category/amount/term codes directly (C1, V2, M3), the row address was spelled out verbatim in the table listing (`hard-threshold-row-category-c1-amount-v2-term-m3`), so there was no need to consult the separate category/amount/term legend docs to translate plain-language values into codes — that step would only be necessary if the question had been phrased in real-world terms instead of the codes themselves.
