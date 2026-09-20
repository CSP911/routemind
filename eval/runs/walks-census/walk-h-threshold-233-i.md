1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m4/body

2. **Answer**:
The CFO signs it off. Yes — three competing quotes plus a written comparison are required before approval. (Delegation limit for this row is 100,047 thousand KRW; 14 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body (flights and hotels → category C3)
- /v1/nodes/hard-threshold-legend-amount/body (about 40 million won → amount V4)
- /v1/nodes/hard-threshold-legend-term/body (until we cancel it → term M4)
- /v1/nodes/hard-threshold-legend-revision/body (confirms current table applies for 2026-09-21)
- /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m4/body (the answer: CFO, three quotes + written comparison)

4. **Notes**:
The three qualifiers (category, amount, term) map to exact wording in the question — "flights and hotels" → C3, "about 40 million won" → V4, "until we cancel it" → M4 — all direct matches, no interpolation needed, which was reassuring given the legends explicitly warn to take the nearest entry when a value isn't listed verbatim.
The real trap was the threshold table's version history: there are three superseded/current versions of this table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the revision-legend page is explicit that "reaching for the newest is wrong for anything before 2026-01-01" and that the oldest version says nothing about being replaced. I checked the revision legend deliberately before trusting `sec-hard-threshold`, since today's date (2026-09-21) needed to be checked against those ranges rather than assumed. It happens to fall in the current range, but skipping that check would have been the way to go wrong silently.
