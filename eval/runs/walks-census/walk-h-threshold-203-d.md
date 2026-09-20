1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m4/body

2. **Answer**: For category C3, amount V1, term M4 (current table, in force from 2026-01-01): the department head signs it off. No, you do not have to get other prices first — competing quotes required: none. (Delegation limit 1035 thousand KRW; 5 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirms which of the three threshold-table versions applies to today's date, 2026-09-20/21)
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m4/body (the answer itself)

4. **Notes**: The procurement area warns up front that "Approval threshold" has three superseded/current versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) and that the oldest version says nothing about being replaced — so grabbing the first threshold table found without checking the legend page would silently give a 2024-era answer. Since today is 2026-09-20/21, the current table (`sec-hard-threshold`, in force from 2026-01-01) is the right one, which is exactly what the legend page's date rule points to. No ambiguity once the legend was checked; the codes C3/V1/M4 in the question matched the row address literally, so no need to consult the separate category/amount/term legend files to translate plain-language descriptions into codes.
