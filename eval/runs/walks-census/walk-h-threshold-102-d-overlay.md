1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C2, amount V1, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, likely holds category/amount/term -> signer mapping" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions, need to confirm which is in force / how to read the table"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_327ef7 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m3/body

2. **Answer**:
The department head signs it off. No, other prices are not required — competing quotes: none. (Delegation limit for this row is 1018 thousand KRW; expect 4 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions is in force for today's date)
- /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m3/body (the actual C2/V1/M3 row: signer, quotes, delegation limit)

4. **Notes**:
The procurement table's listing warned up front that approval-threshold content has three superseded/current versions and pointed at a legend-revision page — worth reading before trusting any row, since the oldest version "says nothing at all about having been replaced." Today's date (2026-09-20 per the task instructions, 2026-09-21 per a later system reminder — either way, after 2026-01-01) falls under the current table, `sec-hard-threshold`, indexed by three qualifiers (category, amount, term), which is exactly the row structure the question gives. Had the question been dated in 2025, the answer would have had to come from `hard-threshold-v2` instead, and grabbing the current table without checking the date would have been the wrong move. No real ambiguity in the row itself — "Competing quotes: none" directly answers the "other prices first" half of the question. One mechanical note: closing the overlay reported the row address as "reached" rather than a named member, since I read it directly under the /v1/nodes/sec-hard-threshold group heading rather than adding it as an explicit overlay member first — didn't affect the outcome, but worth flagging as a minor procedural gap.
