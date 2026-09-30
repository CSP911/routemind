1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dinner with a client, around 12 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/expense "client dinner is a business entertainment expense - need signer and approval rules" --member /v1/regions/procurement "recurring annual spend may be treated as a procurement contract needing threshold approval and competitive quotes" --member /v1/regions/approval "approval chain / signer authority for this amount"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_70f52c --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body

2. **Answer**: The department head signs it off. Yes — three competing quotes are required. (Delegation limit for this row is 20,057 thousand KRW; expect 9 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body

4. **Notes**: The question's three plain-language clauses map onto the three threshold legends almost word for word — "dinner with a client" is category C4, "around 12 million won" is amount V3, and "renewing every year" is term M2 — verbatim matches, not nearest-entry guesses, so there was no ambiguity there. The one place I could have gone wrong was the date: the threshold subject has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the revision-legend page warns explicitly that reaching for the newest is wrong for anything dated before 2026-01-01. Today is 2026-09-21, so the current table (`sec-hard-threshold`) is correct here, but I checked the legend page first rather than assuming, since a 2025-dated question would have needed `hard-threshold-v2` instead. I initially put the question in three regions (expense, procurement, approval) not knowing in advance which one held the threshold table; it turned out to live under procurement, and the expense and approval regions' members were never used.
