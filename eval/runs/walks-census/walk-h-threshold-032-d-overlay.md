1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V4, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches the question directly"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f5e491 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m3/body

2. **Answer**:
Signature required: the division director.
Other prices first: yes — three competing quotes plus a written comparison.
(Context: delegation limit is 100014 thousand KRW, and 13 working days should be expected. This is the current table, in force from 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (established today's date, 2026-09-21, falls under the current version, not the superseded ones)
- /v1/nodes/sec-hard-threshold (located the specific C1/V4/M3 row among 64 rows)
- /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m3/body (the actual answer: signer and quote requirement)

4. **Notes**:
The approval threshold subject has three versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) covering different date ranges, and the legend-revision page is explicit that "reaching for the newest is wrong for anything before 2026-01-01" and the oldest version says nothing about being superseded. Today's date (2026-09-21) falls cleanly in the current version's range, so this wasn't actually ambiguous for this question — but it would have been a trap for a question dated in 2025, where the correct source is the superseded `hard-threshold-v2`, not the current table. I checked the legend before trusting the "current" table rather than assuming recency was safe.

One rough edge: the specific row address (hard-threshold-row-category-c1-amount-v4-term-m3) was never added as a member of the overlay before I read it and closed — I drilled into it directly from the sec-hard-threshold table listing. The close command flagged it as "reached" rather than a named overlay member. Didn't affect the answer, but worth noting that navigating via a table listing bypasses the overlay's own bookkeeping unless you explicitly `overlay add` each address you actually read.
