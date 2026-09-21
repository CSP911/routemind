1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V4, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term lives here per the root table description"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_656403 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold/body /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m1/body

2. **Answer**: For category C1, amount V4, term M1 (current table, in force 2026-01-01 onward): the department head signs it off. Yes, other prices are required first — three competing quotes and a written comparison. (Delegation limit is 100012 thousand KRW; 11 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies for today's date, 2026-09-21)
- /v1/nodes/sec-hard-threshold (current threshold table, in force from 2026-01-01, confirmed the exact row address)
- /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m1/body (the row itself — signer and quote requirement)

4. **Notes**: The question gave the category/amount/term codes (C1, V4, M1) directly, so no trip to the legend-amount/legend-category/legend-term pages was needed to translate plain-language values into codes. The one place this walk could have gone wrong is the threshold table's version history — there are three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and grabbing the first-looking match without checking `hard-threshold-legend-revision` could easily land on the superseded `hard-threshold-v2` table instead of the current `sec-hard-threshold` one. Today's date (2026-09-21) falls after 2026-01-01, so the current table was correct, but this is exactly the kind of question where the newest-looking table needs to be confirmed rather than assumed.
