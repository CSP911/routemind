1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C3, amount V2, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches C3/V2/M4 directly"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ff7024 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body

2. **Answer**:
For category C3, amount V2, term M4 (delegation limit 5,039 thousand KRW), the division director signs it off, and yes — two competing quotes are required before that approval.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three approval-threshold versions applies to today's date, 2026-09-21)
- /v1/nodes/sec-hard-threshold (current table, in force from 2026-01-01, located the per-row address for C3/V2/M4)
- /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body (the actual figures: division director, two competing quotes)

4. **Notes**:
The approval threshold subject has three separate versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) covering different date ranges, and the legend-revision page is explicit that reaching for the newest one is wrong for any date before 2026-01-01 — the oldest version doesn't even say it was superseded, so skipping that check would have been an easy way to silently cite a dead table. Today's date (2026-09-21) falls cleanly in the current table's range, so this walk wasn't actually ambiguous, but the check was necessary rather than a formality: the overlay's initial candidate list included both `hard-threshold-v2` (superseded) and `sec-hard-threshold` (current) side by side with no obvious cue other than reading the legend to know which to trust. Once on the current table, the per-row address pattern (`hard-threshold-row-category-c3-amount-v2-term-m4`) was predictable from the three qualifiers in the question, which made the row easy to spot in a 64-row table.
