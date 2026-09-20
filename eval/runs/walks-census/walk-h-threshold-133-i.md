1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body

2. **Answer**
Sign-off: the CFO. Quotes: yes, three competing quotes plus a written comparison are required. (Delegation limit for this row is 100,031 thousand KRW; 14 working days to expect.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body

4. **Notes**
"A consultant's time" maps to category C2, "about 40 million won" maps to amount V4, and "until we cancel it" maps to term M4 — all three legends had to be checked individually since the row address is built from the three codes and none of the wording in the question matches the row labels directly. The procurement table warned that the threshold table has three superseded versions; I used `/v1/nodes/sec-hard-threshold`, which states it is "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01," and today's date (2026-09-21) falls within that range, so no need to check the older `hard-threshold-v2` or `threshold-table` versions. The easiest mistake to make here would have been picking a nearby amount band (e.g. V3, "around 12 million won") without reading the legend closely — 40 million won is explicitly V4, not a rounding case.
