1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, around 12 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "procurement threshold table covers approval by category, amount and term"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_7141d4 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body

2. **Answer**: The division director signs it off, and yes — three competing quotes are required. (Delegation limit for this row is 20,011 thousand KRW, so 12 million won is within it; 11 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body

4. **Notes**: The mapping was unambiguous here — "a couple of laptops" is a literal entry in the category legend (C1), "around 12 million won" matches "around 12 million won" verbatim in the amount legend (V3), and "until we cancel it" matches the term legend's M4 entry verbatim. No nearest-entry judgment calls were needed, which is unusual and worth flagging in case it signals the question was built directly from these legend rows. The one thing I deliberately did not chase further: `sec-hard-threshold` carries a warning that there are three historical versions of this table (a `hard-threshold-legend-revision` node exists for that), but the table's own header states it is "in force from 2026-01-01" with no end date, and today is 2026-09-21, so I treated it as current without opening the revision legend — that saved a hop but is worth double-checking if the in-force window is ever amended.
