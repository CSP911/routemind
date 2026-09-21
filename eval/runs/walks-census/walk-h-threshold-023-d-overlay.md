1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C1, amount V3, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table since 2026-01-01, by category/amount/term" --member /v1/nodes/hard-threshold-legend-revision "warning about three versions of threshold, need to confirm which applies to today's date"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_9a44c4 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body

2. **Answer**: The division director signs it off. Yes — three competing quotes are required before approval (delegation limit is 20,011 thousand KRW; 11 working days to expect). This is the current table, in force from 2026-01-01, which applies since today's date (2026-09-21) is after that.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions is in force for today's date)
- /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body (the actual figures: signer and quote count)

4. **Notes**: The procurement table listed the current threshold table as `sec-hard-threshold`, but creating the overlay with that as a member expanded it into 66 individual per-row files (one per category × amount × term combination) rather than giving the row directly — the row I needed, `hard-threshold-row-category-c1-amount-v3-term-m4`, was one of them, findable by pattern-matching the address rather than by any table lookup. I read it and the revision-legend directly with `read` rather than adding them as overlay members first, so the close command flagged both as "reached... from somewhere the overlay never named" instead of a clean hit — worth doing `overlay add` next time before reading. The real near-miss was the version question: there are three versions of this table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and the legend explicitly warns that grabbing the newest one is wrong for older dates and that the oldest version doesn't self-report as superseded. Today's date (2026-09-21) falls cleanly in the current-table window, so it wasn't ambiguous here, but skipping that check would have been an easy way to get the row right and the signer/quote count wrong if the question had been dated in 2025.
