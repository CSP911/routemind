1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, about 700,000 won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches a multi-year (3yr) contract for travel-category spend around 700,000 won"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_38f372 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body

2. **Answer**: This is category C3 (flights and hotels), amount V1 (about 700,000 won), term M3 (locked in for three years). Delegation limit for this row is 1034 thousand KRW, so the amount falls within it. It is signed off by the department head. No competing quotes are required. Expect 4 working days.

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body

4. **Notes**: The question's date (today, 2026-09-21) matters here — there are three versions of this threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns that reaching for the newest is wrong for anything dated before 2026-01-01. Today's date puts this squarely in the current table (`sec-hard-threshold`, in force from 2026-01-01), so no ambiguity there, but it would have been an easy trap if the question had been dated in 2025. The three qualifiers (category/amount/term) each have their own legend page and none of them repeat the plain-language description in the row itself — you have to translate "flights and hotels" / "about 700,000 won" / "locked in for three years" into C3/V1/M3 before the row address can even be constructed, and the row list only shows codes, not the underlying scenario, so guessing an address without reading all three legends first would have been wrong.