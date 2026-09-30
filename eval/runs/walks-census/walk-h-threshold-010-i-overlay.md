1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, roughly 3 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold and quote requirements for a one-time equipment purchase around 3M KRW"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d3846d --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body

2. **Answer**:
The team lead signs it off. Yes, two competing quotes are required. (This falls under category C1 "a couple of laptops", amount V2 "roughly 3 million won", term M1 "just the once" — delegation limit for this row is 5,004 thousand KRW, so the ~3 million won purchase is within the team lead's authority; expect 5 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body

4. **Notes**:
The procurement region's opening table surfaces a loud warning that the approval threshold has three versions with overlapping-looking date ranges (`hard-threshold-legend-revision`, `hard-threshold-v2` superseded, and the current `sec-hard-threshold`). It would be easy to grab the superseded 2024-07-01–2025-12-31 version by mistake since it's listed right next to the current one with no obvious flag until you read the "WARNING" text. I confirmed the current table (`sec-hard-threshold`) states it's in force from 2026-01-01, which covers today's date (2026-09-21), so I used that one and didn't need to open the legend-revision or v2 documents.

The three legends (category/amount/term) are each phrased as translations of plain-language qualifiers into row codes, and the row address is only findable by combining all three codes yourself (c1/v2/m1) — the table listing never spells out that combination in its row descriptions, so it's on the reader to assemble the address correctly.

Minor oddity: `overlay close` reported all four used addresses as "reached ... answered from somewhere the overlay never named," presumably because I only added the procurement region as a formal overlay member and then navigated on to child tables/files without `overlay add`-ing each one. Didn't affect the answer, just a bookkeeping quirk of how I used the tool.
