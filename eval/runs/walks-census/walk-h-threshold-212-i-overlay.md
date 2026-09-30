1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, roughly 3 million won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount + term + category threshold and quote requirement questions" --member /v1/regions/expense "travel spend could also be governed by expense policy"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_cb31cf --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m3/body

2. **Answer**
The department head signs it off. Two competing quotes are required. (Delegation limit for this row is 5,038 thousand KRW; expect 7 working days.) This is category C3 (flights and hotels), amount band V2 (roughly 3 million won), term M3 (locked in for three years), from the approval threshold table in force from 2026-01-01.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (established which version is current for today's date, 2026-09-21)
- /v1/nodes/hard-threshold-legend-category/body (mapped "flights and hotels" → category C3)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "roughly 3 million won" → amount V2)
- /v1/nodes/hard-threshold-legend-term/body (mapped "locked in for three years" → term M3)
- /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m3/body (the row with the answer: department head, two quotes)

4. **Notes**
The question's wording ("roughly 3 million won", "locked in for three years") turned out to be lifted almost verbatim from the amount and term legend rows — that made mapping unambiguous once I found the legends, but it would have been easy to skip the legend step and guess at a category/amount/term combination directly from the row list, since the row addresses themselves only show codes (c3-v2-m3) with no plain-language meaning. The real risk was the approval-threshold versioning: there are three versions of this table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and the legend-revision doc explicitly warns that reaching for the newest is wrong unless the question's date warrants it. Today is 2026-09-21, so the current table (`sec-hard-threshold`) was correct, but I made a point of reading the revision-legend first rather than assuming — this is exactly the kind of question the doc warns is easy to get wrong for a 2025-dated question. I did not end up needing the expense-region member (travel-expense, corp-card, etc.) — the question was about contract approval/signing authority and quote requirements, which lives in procurement, not expense reimbursement, even though the underlying spend (flights/hotels) sounds like a travel expense.
