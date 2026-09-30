1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V4, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term lives here"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f39bf9 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body

2. **Answer**: The CFO signs it off. Yes — three competing quotes plus a written comparison are required before this goes to signature. (Delegation limit for this row is 100015 thousand KRW; 14 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/sec-hard-threshold
/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body

4. **Notes**: The approval-threshold subject has three versions in force at different dates (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend page warns explicitly that reaching for the newest table is wrong for anything dated before 2026-01-01 — the oldest version doesn't even say it was superseded. Today's date (2026-09-21) falls in the current window, so `sec-hard-threshold` was correct, but this is exactly the kind of question where grabbing the first threshold-looking table without checking the legend would have silently given a stale answer for a differently-dated question. Once in the current table, C1/V4/M4 was a direct, unambiguous row lookup — no confusion there. The overlay close command reported all three used addresses as "reached" rather than as matched overlay members, since I only added the procurement region as a member and then read further pages directly instead of adding each one to the overlay — functionally fine, but worth noting the tool distinguishes "in the overlay" from "reached while answering."
