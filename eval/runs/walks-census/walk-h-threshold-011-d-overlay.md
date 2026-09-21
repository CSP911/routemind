1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V2, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "starting point for procurement approval threshold questions"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_86cb22 --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body

2. **Answer**: The department head signs it off. Yes — two competing quotes are required before approval. (Delegation limit for this row is 5,005 thousand KRW; 6 working days to expect.)

3. **Source**: /v1/nodes/sec-hard-threshold (table, to locate the row) → /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body (the row itself, source of the answer).

4. **Notes**: The procurement table flagged that the approval threshold has THREE versions with a legend-revision warning (`hard-threshold-legend-revision`, `hard-threshold-v2` superseded 2024-07-01–2025-12-31). I did not open the legend-revision or the superseded v2 doc because `sec-hard-threshold` states plainly it is "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01," and today is 2026-09-21, so the current table is the right one — but this is the kind of question where grabbing the superseded `hard-threshold-v2` row by mistake would have given a wrong (and different) answer. Worth double-checking the effective date next time rather than assuming. Also, the exact row address (category-c1-amount-v2-term-m2) was printed directly by the table listing, so no need to open the amount/category/term legend files to decode codes — the codes in the question matched the row-naming convention exactly. One oddity: `overlay close` reported the two addresses I used as "reached" rather than "member," since I hadn't added them to the overlay with `add` first — only closed with `--used`. Answer not affected, but the overlay bookkeeping wants explicit `add` calls if you want them recorded as proper members.
