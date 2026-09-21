1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C4, amount V3, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, in force since 2026-01-01, today is 2026-09-20" --member /v1/nodes/hard-threshold-legend-revision/body "warns there are three versions of the threshold table with different date ranges; need to confirm which applies"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a6185c --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body

2. **Answer**: The department head signs it off. Yes — three competing quotes are required before this can go through. (Delegation limit is 20,057 thousand KRW; working days to expect is 9.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed today's date, 2026-09-20, falls under the current table, not the two superseded versions)
- /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body (the actual figures)

4. **Notes**: The procurement region table carries a loud warning that approval-threshold has three versions with different date ranges (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-20) clearly falls in the current, three-qualifier version (`sec-hard-threshold`), so the newest table was in fact correct here — but the warning is explicit that this isn't always true, so I read the revision legend before trusting the row rather than assuming. The overlay's `close` output flagged the target row as "reached = answered from somewhere the overlay never named" — I had added the parent table and the revision legend as members but never explicitly `overlay add`'d the specific C4/V3/M2 row before reading it, since it was already visible as a child listing under the table member. That's a mechanical note about how I used the tool, not an ambiguity in the answer itself.
