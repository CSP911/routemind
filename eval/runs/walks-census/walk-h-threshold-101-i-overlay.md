1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A consultant's time, about 700,000 won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "recurring service contract ~700,000 won - approval threshold by amount/category/term is a procurement question"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8047b3 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body
```

2. **Answer**
The team lead signs it off. No competing quotes are needed (Competing quotes: none). This is for category C2 (a consultant's time), amount V1 (about 700,000 won), term M2 (renewing every year), delegation limit 1,017 thousand KRW, working days to expect: 3. This is the current table, in force from 2026-01-01.

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "about 700,000 won" → amount V1)
- /v1/nodes/hard-threshold-legend-term/body (mapped "renewing every year" → term M2)
- /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body (the answer: team lead, no competing quotes)

4. **Notes**
- The `sec-hard-threshold` table is explicitly marked as "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01" and there's a loud warning node (`hard-threshold-legend-revision`) that the approval threshold has THREE versions. Today's date (2026-09-21) falls after 2026-01-01, so the current table was the right pick without needing to check the superseded `hard-threshold-v2` (2024-07-01 to 2025-12-31) or the older `threshold-table`. Easy to get this wrong if the date check is skipped.
- The row table under `sec-hard-threshold` has 64 rows (4 categories × 4 amounts × 4 terms), none of it self-explanatory from the row address alone — you must resolve category/amount/term through the three separate legend files first, then compose the address (`hard-threshold-row-category-c2-amount-v1-term-m2`). The row addresses are printed in the table listing, so I selected the matching one rather than constructing it freely.
- The `overlay close` call reported all four addresses as "reached ... answered from somewhere the overlay never named" rather than as members I had formally added with `overlay add`. I never ran `overlay add` for the legend/row addresses — I jumped straight to `read` after finding them in the `sec-hard-threshold` table listing. Functionally the answer is unaffected, but the working set wasn't kept fully up to date as instructed.
