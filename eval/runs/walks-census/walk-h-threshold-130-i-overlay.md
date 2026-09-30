1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Consultant time, about 40 million won, one-time: whose signature is needed, and are other price quotes required first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches consulting/one-time service spend"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_0eb946 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body

2. **Answer**: The department head must sign it off, and yes — three competing quotes plus a written comparison are required first. (Delegation limit for this row is 100,028 thousand KRW; expect 11 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies to today's date, 2026-09-21)
- /v1/nodes/hard-threshold-legend-category/body (consultant's time → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (about 40 million won → amount V4)
- /v1/nodes/hard-threshold-legend-term/body (just the once → term M1)
- /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body (the answering row: signer and quote requirement)

4. **Notes**: The approval threshold subject has three superseded/current versions on record, and the legend-revision page warns explicitly that reaching for the newest version is wrong for any question dated before 2026-01-01 — the oldest version doesn't even say it was replaced. Today's date (2026-09-21) falls after the 2026-01-01 cutover, so the current table (`sec-hard-threshold`) was correct here, but this is exactly the kind of question where grabbing the first "approval threshold" hit without checking the revision legend would silently give a stale answer. The row itself is only reachable by resolving three independent legends (category, amount, term) into codes — none of the three qualifiers can be guessed from the question's wording alone, they have to be looked up one at a time.
