1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body

2. **Answer**: The team lead signs it off. No competing quotes are needed (delegation limit 1,000 thousand KRW covers this; expect 2 working days). This is under the current approval threshold table (in force from 2026-01-01), which applies since today is 2026-09-20.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body

4. **Notes**: The revision-legend warning was the one place a wrong turn was live — three versions of this table exist, and the note explicitly flags that for a 2025-dated question the middle version (`hard-threshold-v2`) is correct, not the current one. Today's date (2026-09-20) put it past that trap into the current table (`sec-hard-threshold`), but it would have been easy to grab the current table on reflex without checking. The three legends (category/amount/term) were needed to translate the plain-language question ("a couple of laptops", "about 700,000 won", "just the once") into the C1/V1/M1 row code — none of the wording is guessable without reading them, since e.g. "about 700,000 won" only maps to V1 via the amount legend's explicit table.
