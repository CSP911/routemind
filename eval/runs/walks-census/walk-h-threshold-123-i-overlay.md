1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Consultant service contract, ~12M KRW, ongoing until cancelled: whose signature is needed, and are competitive quotes required first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches consulting spend and contract term question"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_7f6302 --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body

2. **Answer**: The division director signs it off, and yes — three competing quotes are required first. (Delegation limit for this row is 20,027 thousand KRW; expect 11 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "around 12 million won" → amount V3)
- /v1/nodes/hard-threshold-legend-term/body (mapped "until we cancel it" → term M4)
- /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body (the row itself: division director, three competing quotes)

4. **Notes**: The three legend tables (category, amount, term) had to be read separately to translate the plain-language question into the C2/V3/M4 row code — none of this mapping is written on the row itself, and skipping any one of the three legends would make it impossible to pick the right row out of 64. The amount phrase "around 12 million won" was a verbatim match to the legend's "around 12 million won" (V3), so no rounding judgment was needed there. Likewise "until we cancel it" matched the term legend's M4 entry verbatim. The procurement table also listed a superseded `hard-threshold-v2` (in force 2024-07-01 to 2025-12-31) alongside the current `sec-hard-threshold` (in force from 2026-01-01) — today being 2026-09-21, the current table was clearly the right one, but it would be easy to grab the wrong version if not careful about the in-force dates stated on each row.
