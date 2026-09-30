1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C3, amount V3, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term, in force since 2026-01-01" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold table has three versions - need to confirm which applies for today's date"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c1ce47 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body

2. **Answer**:
For category C3, amount V3, term M4 (current table, in force from 2026-01-01): the division director signs it off, and yes — three competing quotes are required first. Delegation limit is 20,043 thousand KRW; 11 working days to expect.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three table versions applies today)
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body (the answer)

4. **Notes**:
The threshold table has three superseded-but-not-withdrawn versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page is explicit that reaching for the newest is wrong for a question dated before 2026-01-01 — the oldest version doesn't even say it was replaced. Today's date (2026-09-21/2026-09-20 depending on source) is well past 2026-01-01, so the current table applied without ambiguity here, but this is clearly a trap for questions dated in 2025 or earlier, where the middle version would be correct instead. Opening the procurement area table already showed the exact row address (category-c3-amount-v3-term-m4), so no separate legend lookups for amount/category/term banding were needed — the qualifiers were given directly in the question rather than needing to be derived from a value. One bookkeeping note: the row address was never explicitly added to the overlay via `overlay add`, so the close command reported it as "reached" (answered from somewhere the overlay never named) rather than as a named member — harmless here since it closed cleanly, but worth adding explicitly next time to keep the working set accurate.
