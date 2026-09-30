1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V2, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_9e4ad3 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body

2. **Answer**
For category C4, amount V2, term M2: signs it off — the department head. Yes, other prices are required first — two competing quotes. (Delegation limit 5,053 thousand KRW; working days to expect: 6.)

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions applies for today's date, 2026-09-21)
- /v1/nodes/sec-hard-threshold (current threshold table, in force from 2026-01-01, listing the C4/V2/M2 row)
- /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body (the row itself — answer came from here)

4. **Notes**
The approval threshold subject has three superseded/current versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns that "the oldest says nothing at all about having been replaced" — so grabbing the first-looking match without checking the date would have silently returned a stale answer. Today's date (2026-09-21) falls in the 2026-01-01-onwards band, so the current table `sec-hard-threshold` was correct, but this is exactly the kind of question where reaching for the newest table without checking is only accidentally right — it's right here because the date happens to be after 2026-01-01, not because "current" is a safe default in general. No other ambiguity: C4/V2/M2 has one exact matching row in the current table, and it stated both the signer and the quote requirement directly.
