1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A consultant's time, around 12 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "one-time purchase over a threshold - approval signature and competitive quote requirement is procurement's domain"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8e9984 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body

2. **Answer**
The department head signs it off. Yes — three competing quotes are required. (Delegation limit for this row is 20,024 thousand KRW; working days to expect: 8.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body

4. **Notes**
The procurement region table surfaced a warning that the approval threshold table has three historical versions (`hard-threshold-legend-revision`) plus a superseded `hard-threshold-v2` (2024-07-01 to 2025-12-31). I stuck with `sec-hard-threshold`, labeled as the current table in force from 2026-01-01, since today's date (2026-09-21) falls inside that window — but it would have been easy to grab the superseded v2 row by mistake since both tables have near-identical row-address naming (`hard-threshold-row-category-...` vs the v2 equivalent) and the WHY-column truncation doesn't make the version difference obvious until you read the legend-revision doc or notice the "in force from" line at the bottom of the row itself.
The row itself required three separate legend lookups (category, amount, term) to translate the plain-language question into the C2/V3/M1 code before the actual row address could be constructed from the table listing — no shortcut around that, and the codes must match exactly or you land on the wrong row silently.
The overlay close reported all four used addresses as "reached... from somewhere the overlay never named" since I only added the parent /v1/regions/procurement as a member and then drilled down freely rather than adding each intermediate address to the overlay — functionally fine since the close still recorded them, but worth flagging in case future walks are expected to `add` each hop explicitly.
