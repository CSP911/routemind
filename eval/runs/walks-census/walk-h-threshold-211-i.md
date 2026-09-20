1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body

2. **Answer**
The department head signs it off. Yes — two competing quotes are required first. (Delegation limit for this row is 5,037 thousand KRW; expect 6 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body

4. **Notes**
The three plain-language values in the question ("flights and hotels", "roughly 3 million won", "renewing every year") map exactly to phrases used verbatim in the three legend tables (category C3, amount V2, term M2), so no interpolation was needed — that's a relief given the legends explicitly say to pick the nearest entry when a value isn't listed. The main risk was version confusion: the procurement table listed a `hard-threshold-legend-revision` warning about three versions of the approval-threshold table, and a superseded `hard-threshold-v2` row set (in force 2024-07-01 to 2025-12-31) sits right next to the current one in the listing. Today's date (2026-09-21) is well past the current table's 2026-01-01 effective date, so I used `sec-hard-threshold` and did not need to open the legend-revision or superseded pages — but it would be easy to grab the wrong version by pattern-matching on the similar node names (`hard-threshold-v2` vs. the current table's row addresses, which also contain "v2" for amount-band V2 — those "v2"s are unrelated to each other and could easily be confused).
