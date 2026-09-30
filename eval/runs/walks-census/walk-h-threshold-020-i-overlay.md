1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, around 12 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "laptops purchase is a procurement/equipment spend, need approval threshold and whether competing quotes are required"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f98dbf --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**:
The department head signs it off, and yes — three competing quotes are required. (Delegation limit for this row is 20,008 thousand KRW, so the 12 million won purchase falls within it.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body (mapped "a couple of laptops" → category C1)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "around 12 million won" → amount V3)
- /v1/nodes/hard-threshold-legend-term/body (mapped "just the once" → term M1)
- /v1/nodes/hard-threshold-legend-revision/body (confirmed the current table, in force 2026-01-01 onwards, is the correct version for today's date)
- /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body (the answer: department head signs, three competing quotes)

4. **Notes**:
The three-legend indirection (category / amount / term each mapped separately before the row address could be built) is easy to rush — each legend explicitly warns "this table is the only place the mapping is written down," which is the cue to stop guessing the row name and go read all three first. The revision-legend check mattered here too: the table under /v1/nodes/sec-hard-threshold is explicitly labeled "current" and in force from 2026-01-01, but the legend page warns not to reach for the newest table blindly and that for a 2025-dated question the middle version would apply instead. Today's date is well past 2026-01-01 so the current table was correct, but this is clearly the trap the walk is testing for — I checked the revision legend deliberately rather than assuming "current" meant "correct for any date."
