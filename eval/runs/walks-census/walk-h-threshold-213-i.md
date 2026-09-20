1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body

2. **Answer**
Signature required: the division director.
Competing quotes required first: yes, two.
(Delegation limit for this row: 5,039 thousand KRW; expect 8 working days.)

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (maps "flights and hotels" → category C3)
- /v1/nodes/hard-threshold-legend-amount/body (maps "roughly 3 million won" → amount V2)
- /v1/nodes/hard-threshold-legend-term/body (maps "until we cancel it" → term M4)
- /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body (the answer: division director, two quotes)

4. **Notes**
The procurement region table listed both a current table (`sec-hard-threshold`, in force since 2026-01-01) and superseded versions (`hard-threshold-v2`, and one older still per `hard-threshold-legend-revision`). Today's date (2026-09-21) falls inside the current table's validity window, so I used `sec-hard-threshold` and never needed to open the superseded rows or the revision-legend file — but it would have been easy to grab the wrong version if the date check were skipped. The three-legend indirection (category/amount/term each map plain-language phrasing to a code letter+number) is not obvious from the top-level table alone; each legend explicitly says "this table is the only place the mapping is written down," so skipping any one of them would make it impossible to construct the correct row address. Note the row address is built only from codes already printed by the legends (c3/v2/m4) — never guessed.
