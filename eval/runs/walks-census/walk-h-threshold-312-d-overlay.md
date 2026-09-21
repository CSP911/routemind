1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C4, amount V2, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term, in force since 2026-01-01, likely has C4/V2/M3 row" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold table has three versions - need to confirm which version applies for today's date" --member /v1/nodes/purchase-request "how many quotes needed - purchase request table may define quote requirements"
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2842b5 --outcome answered --used /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**:
For category C4, amount V2, term M3 (delegation limit 5,054 thousand KRW): the department head signs it off, and yes — two competing quotes are required first. Expect 7 working days.

3. **Source**:
- /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body (the row itself: signer, quote count, delegation limit, turnaround)
- /v1/nodes/hard-threshold-legend-revision/body (confirms this current table, in force from 2026-01-01, is the correct version for today's date 2026-09-21, not the two superseded versions)

4. **Notes**:
This walk was straightforward because the C4/V2/M3 row name matched the question's category/amount/term literally, so I didn't need the amount/category/term legends to interpret ambiguous bands — I went straight to the named row. The one thing worth flagging: the procurement table's warning that "approval threshold has THREE versions" made me stop and explicitly check the revision legend before trusting the row, even though the row itself already states "In force from 2026-01-01" and today (2026-09-21) is well within that range — no real ambiguity, but the table's warning text is loud enough that skipping the check would have felt sloppy. Also worth noting: I included /v1/nodes/purchase-request as an overlay member expecting a general "how many quotes" table, but the answer came entirely from the specific threshold row instead, so that member went unused — the overlay closer reported the threshold row as "reached" rather than "member" since I read it via its exact address rather than the sec-hard-threshold table member I'd actually added, which is a harmless quirk of how I passed --used, not a real discrepancy.
