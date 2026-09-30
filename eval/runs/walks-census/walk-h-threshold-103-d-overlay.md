1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C2, amount V1, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches the question directly"
./bench/rmcli.py overlay remove --id ov_2026-09-21_6e36ee --address /v1/nodes/contract-custody --why "not relevant to threshold signature question"  [failed: 404, address not in overlay — abandoned pruning]
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6e36ee --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold/body /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body

2. **Answer**:
The department head signs it off. No competing quotes are required (quotes needed: none). Delegation limit for this row is 1,019 thousand KRW; working days to expect: 5.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold versions applies to today's date, 2026-09-21)
/v1/nodes/sec-hard-threshold/body (current table, in force from 2026-01-01, listing the row addresses)
/v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body (the actual answer)

4. **Notes**:
The overlay-remove call failed with a 404 saying the address "is not in this overlay" — I had copy-pasted the address exactly as printed in the table, so it's not a typo issue; the printed rows from `table /v1/regions/procurement` weren't all registered as removable overlay members the way I expected. Rather than fight the overlay's bookkeeping I abandoned pruning and just fetched what I needed directly, which cost nothing since the tool is read-only-safe.

The one place this walk could have gone wrong: there are THREE historical versions of the approval-threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page explicitly warns that "reaching for the newest is wrong for anything before 2026-01-01" and that the oldest version says nothing about being superseded. Today's date (2026-09-21) falls after the 2026-01-01 cutover, so `sec-hard-threshold` is correct — but this is exactly the kind of question where grabbing the first plausible-looking threshold table without checking the effective date would give a stale answer. Since the current table happened to have an exact row for C2/V1/M4, no legend lookups for the category/amount/term codes were needed — the question already gave codes, not descriptions.

The overlay close output flagged the row address as "reached" rather than a formally-used named member ("answered from somewhere the overlay never named") because I read it directly instead of adding it via `overlay add` first — cosmetic, didn't affect the outcome.
