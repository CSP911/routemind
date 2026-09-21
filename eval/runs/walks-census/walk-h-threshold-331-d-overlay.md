1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V4, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term — matches C4/V4/M2 exactly"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c0068d --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m2/body

2. **Answer**:
The division director signs it off. Yes — three competing quotes and a written comparison are required before this can be approved (delegation limit 100,061 thousand KRW, 12 working days to expect).

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold versions applies to today's date)
/v1/nodes/sec-hard-threshold (current threshold table, in force from 2026-01-01, to locate the C4/V4/M2 row)
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m2/body (the row itself — signer and quote requirement)

4. **Notes**:
The approval threshold subject has three separate versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns explicitly that "the oldest says nothing at all about having been replaced" — reaching for the newest table without checking would have been silently wrong for a question dated in 2025, and reaching for the oldest would be wrong for one dated today. Today (2026-09-21) falls after 2026-01-01, so the current table (`sec-hard-threshold`) was correct, but this required an explicit date check rather than assuming the newest is always right. No ambiguity in the row itself — C4/V4/M2 mapped directly to one row with no interpretation needed.
