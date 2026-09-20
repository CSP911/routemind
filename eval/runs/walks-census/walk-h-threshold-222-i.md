1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m3/body

2. **Answer**
The division director signs it off. Yes — three competing quotes are required first. (Delegation limit for this row is 20,042 thousand KRW; expect about 10 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m3/body

4. **Notes**
"Flights and hotels, ~12 million won, locked in for three years" isn't itself a row — it has to be translated through three separate legends (category, amount, term) into codes C3/V3/M3 before the actual row can be addressed, and none of those codes can be guessed or constructed; each legend spells out its own mapping explicitly. The near-miss here was the threshold table's version history: there are three superseding versions of this table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page is explicit that reaching for "the newest" is only correct if the question's date actually falls in the newest window — for a 2025-dated question the answer would have been the middle version instead. Today (2026-09-20/21) falls after 2026-01-01, so `sec-hard-threshold` was the right table, but this is clearly the trap the walk is built to test.
