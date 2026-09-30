1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C2, amount V2, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term lives here"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_684853 --outcome answered --used /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body

2. **Answer**: For category C2, amount V2, term M3: the department head signs it off, and yes — two competing quotes are required first. (Delegation limit 5,022 thousand KRW; 7 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies to today's date, 2026-09-21)
- /v1/nodes/sec-hard-threshold (current threshold table, in force from 2026-01-01, listed the row addresses by category/amount/term)
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body (the actual answer: signer and quote requirement)

4. **Notes**: The approval-threshold subject has three versions in RouteMind (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onwards), and the legend-revision page explicitly warns that the oldest version never says it was superseded — reaching for the newest table without checking dates would be wrong for a 2025-dated question. The question here carries no explicit date, so I used today's date (2026-09-21) to select the current table (`sec-hard-threshold`), which is also the version indexed by all three qualifiers (category, amount, term) matching the question's phrasing exactly — a good sanity check that this was the right version. One process note: the overlay's `used` addresses on close were reported as "reached... from somewhere the overlay never named" because I read the threshold-table listing and the specific row directly rather than first adding them via `overlay add`; the overlay itself only ever held the top-level `/v1/regions/procurement` member. This didn't affect the answer but is worth flagging since the tool distinguishes formally-tracked members from addresses merely visited.
