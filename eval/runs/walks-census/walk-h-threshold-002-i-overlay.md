1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two laptops, ~700,000 won, 3-year lock-in: whose signature, and need competing quotes?" --member /v1/regions/procurement "approval threshold by category/amount/term is the procurement table's stated purpose"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c66c9f --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body

2. **Answer**: The department head signs it off. No competing quotes are required. (Delegation limit for this row is 1,002 thousand KRW; working days to expect: 4.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body

4. **Notes**: The approval-threshold subject has three superseded/current versions gated by date, and the legend-revision page explicitly warns that the oldest version says nothing about being replaced — reaching for the newest table without checking the date would be wrong for a 2025-dated question, and reaching for the oldest would be wrong for a 2025-dated question too. Today (2026-09-21) falls after the 2026-01-01 cutover, so the current table (`sec-hard-threshold`) was correct, but this was a deliberate check, not an assumption. The row itself is indexed by three qualifiers (category, amount, term) that must each be translated through a separate legend page — "a couple of laptops" → C1, "about 700,000 won" → V1, "locked in for three years" → M3 — matching the question's wording verbatim to the legend's left-hand column rather than guessing at bands. The final overlay-close reported the used addresses as "reached... from somewhere the overlay never named" because I read them directly via `read`/table navigation rather than first adding each as an explicit overlay member — worth noting for future walks: narrowing the overlay's member list to match exactly what gets used would avoid that note, though it didn't affect the answer.
