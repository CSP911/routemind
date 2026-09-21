1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, roughly 3 million won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "procurement threshold by category/amount/term matches this question"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3601bc --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body

2. **Answer**: The department head signs it off, and yes — two competing quotes are required. (Delegation limit for this row is 5,006 thousand KRW; working days to expect: 7.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body (mapped "a couple of laptops" → category C1)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "roughly 3 million won" → amount V2, an exact match)
- /v1/nodes/hard-threshold-legend-term/body (mapped "locked in for three years" → term M3, an exact match)
- /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body (the row: department head signs, two competing quotes)

4. **Notes**: Nothing here required guessing at nearest-band values — "roughly 3 million won" and "locked in for three years" landed on exact legend entries (V2 and M3 respectively), unlike a fuzzier amount would have. The one thing worth flagging: `sec-hard-threshold` is explicitly labeled the *current* table (in force from 2026-01-01), and a sibling node (`hard-threshold-legend-revision`) warns there are three historical versions of this table. I didn't need to open that legend since today's date (2026-09-20/21) falls inside the current table's in-force window and the row itself restates that window, but a careless walk could have grabbed `hard-threshold-v2` (the superseded 2024-07-01 to 2025-12-31 version) from the earlier overlay listing by pattern-matching the "v2" in its name against nothing to do with amount code V2 — the naming is confusable and worth a second look before reading the wrong row.
