1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, about 40 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount, and term for procurement — laptops purchase around 40M won on an ongoing/until-cancelled term"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_618b66 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body

2. **Answer**: The CFO signs it off. Yes — three competing quotes and a written comparison are required first. (Delegation limit for this row is 100,015 thousand KRW, so the 40M won purchase is within this row's limit, not an excess case.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body (laptops → category C1)
- /v1/nodes/hard-threshold-legend-amount/body (about 40 million won → amount V4)
- /v1/nodes/hard-threshold-legend-term/body ("until we cancel it" → term M4)
- /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body (the row itself: CFO, three quotes + written comparison)

4. **Notes**: The path from the top-level table to the answer was mechanical once I recognized this as a procurement-threshold question — the legends translate the plain-language description ("a couple of laptops", "about 40 million won", "until we cancel it") into the C1/V4/M4 codes almost word-for-word, so there was little room to pick the wrong row. The one thing worth flagging: the procurement table's row listing carries an explicit warning that there are three historical versions of the threshold table (`hard-threshold-v2` superseded 2024-07-01–2025-12-31, an older `threshold-table` before that, and the current `sec-hard-threshold` in force from 2026-01-01). Today's date (2026-09-21) falls inside the current version's range, so I used `sec-hard-threshold`/its row directly, but it would have been easy to grab the superseded `hard-threshold-v2` row by mistake if I hadn't checked the effective date against today. I did not need to consult the older versions or the legend-revision doc beyond confirming the current table applies.
