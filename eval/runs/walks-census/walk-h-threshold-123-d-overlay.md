1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C2, amount V3, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term, in force since 2026-01-01, today is 2026-09-21" --member /v1/nodes/hard-threshold-legend-revision/body "warns approval threshold has three versions with different effective dates - need to confirm which applies today"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3a86d9 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body

2. **Answer**:
The division director signs it off. Yes, other prices are required first: three competing quotes. (Delegation limit for this row is 20,027 thousand KRW; 11 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body

4. **Notes**:
The procurement area lists three vintages of the approval-threshold subject (`threshold-table`, `hard-threshold-v2`, and the current `sec-hard-threshold`), and the legend-revision page is explicit that reaching for the newest is wrong for a date before 2026-01-01. Today is 2026-09-21, which is after that cutoff, so the current three-qualifier table (`sec-hard-threshold`) is the right one — but this is exactly the kind of question where grabbing the first threshold-looking hit without checking the date would silently give the wrong signer. Worth flagging: when I created the overlay by naming the `sec-hard-threshold` table as a member, it expanded into all 64 individual category/amount/term rows plus the three legend pages, so the specific C2/V3/M4 row was already sitting in the working set before I picked it — the overlay-close output noted it as "reached" rather than an explicitly-named member, which is just bookkeeping, not an error, but worth knowing that adding a table pulls in everything under it.
