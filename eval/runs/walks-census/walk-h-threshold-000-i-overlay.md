1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, about 700,000 won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold and quote requirement by amount/category for a one-time purchase"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b98169 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body

2. **Answer**: The team lead signs it off. No competing quotes are needed ("Competing quotes: none"). Expect 2 working days. (Delegation limit for this row is 1,000 thousand KRW, i.e. 1,000,000 won, which comfortably covers the ~700,000 won purchase.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body — maps "a couple of laptops" to category C1
- /v1/nodes/hard-threshold-legend-amount/body — maps "about 700,000 won" to amount V1
- /v1/nodes/hard-threshold-legend-term/body — maps "just the once" to term M1
- /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body — the row itself: team lead signs, no competing quotes required, in force from 2026-01-01 (current as of today, 2026-09-21)

4. **Notes**: The procurement region table flagged that the approval-threshold document has three versions (`hard-threshold-legend-revision` warns of this), so I made sure to use `sec-hard-threshold`, explicitly labeled as "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01" — not the superseded `hard-threshold-v2`, which is easy to grab by mistake since it sorts near the current one and looks equally official. The legend tables translate the question's plain-English phrasing ("a couple of laptops," "about 700,000 won," "just the once") almost verbatim into category/amount/term codes, which made the row lookup unambiguous. One oddity: `overlay close` marked all four addresses I used as "reached" rather than tracked members, with a note that they were "answered from somewhere the overlay never named" — I never called `overlay add` for the specific file addresses (only had the parent `/v1/regions/procurement` as a member), so the tool couldn't credit them as formal members of the working set even though they're exactly what answered the question. Worth calling `overlay add` for leaf addresses as I visit them next time, not just the initial region.
