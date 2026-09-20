1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body

2. **Answer**
The department head signs it off. No, you do not need to get other prices first — competing quotes required: none. (Delegation limit for this row is 1,050 thousand KRW; expect 4 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body

4. **Notes**
The procurement table warns up front that the approval-threshold subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) and that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-21) falls under the current table (`sec-hard-threshold`, in force from 2026-01-01), so no adjustment was needed here — but this is exactly the kind of question where grabbing the first "approval threshold" hit without checking the revision legend would have risked citing the wrong version had the question been dated differently. I checked the legend explicitly before opening the row to be sure. The row address itself was printed verbatim by the `sec-hard-threshold` table listing (`hard-threshold-row-category-c4-amount-v1-term-m3`), so no address was constructed by hand.
