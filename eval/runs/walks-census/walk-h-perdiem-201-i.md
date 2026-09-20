1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 227 USD per night. Receipt required above 29 USD (the receipt threshold for this row). This is grade G3 (department head), band B1 (Tokyo), stay S2 (four nights), under the current overseas per-diem table in force since 2026-01-01.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → B1)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → S2)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body (lodging 227 USD/night, receipt threshold 29 USD)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms today, 2026-09-20, falls under the current table, not the two superseded versions)

4. **Notes**:
The expense region's table blurb explicitly warns that the overseas per-diem "current table since 2026-01-01" coexists with older superseded band-only caps still present in the same area (`hard-perdiem-v2`, `overseas-rates`), and the region table itself surfaces a `hard-perdiem-legend-revision` file up front — that's a deliberate trap for grabbing the wrong row by date. Checked the revision legend last to be sure 2026-09-20 lands in the current table rather than assuming the newest table is always right. The three legends (grade/band/stay) have to be read in full each time — nothing about "department head," "Tokyo," or "four nights" is guessable from the row addresses themselves ("take the nearest entry above it" caveat in each legend also means a mismatch wouldn't error loudly, it would silently give the wrong row). No separate general "evidence" receipt threshold was consulted — the per-diem row states its own receipt threshold (29 USD) directly, which is what answers the question as asked.
