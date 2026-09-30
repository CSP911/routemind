1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Dinner with a client, about 40 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - likely gives signer and quote requirement" --member /v1/regions/expense "client dinner could be an entertainment/business expense, not procurement" --member /v1/nodes/purchase-request "purchase request process, may state how many quotes are needed"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_74d6ce --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body

2. **Answer**
The CFO signs it off. Yes — three competing quotes and a written comparison are required. (Delegation limit for this row: 100,063 thousand KRW; expect 14 working days.)

Derivation: "dinner with a client" maps to category C4; "about 40 million won" maps to amount band V4; "until we cancel it" (no fixed end, not annual renewal, not a 3-year lock-in) maps to term M4. Today's date (2026-09-21) falls under the current threshold table (in force since 2026-01-01, indexed by category/amount/term), so the row category-C4/amount-V4/term-M4 applies, not either of the two superseded versions.

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body

4. **Notes**
The question's phrasing is deliberately indirect and maps to the threshold table's three legends almost word-for-word: "dinner with a client" is the exact example given for category C4, "about 40 million won" is the exact example for amount V4, and "until we cancel it" is the exact example for term M4 — so once the legends were read, the row selection was unambiguous. The one place I nearly went wrong was starting down the expense/entertainment-reimbursement path (I added /v1/regions/expense to the working set) before realizing the question isn't about reimbursing a receipt after the fact — it's about approving a spend commitment before it happens, which is squarely procurement/threshold territory, not expense. The expense-region member turned out unused. I also deliberately checked hard-threshold-legend-revision before trusting sec-hard-threshold, since the table area explicitly warns that three versions of this table exist and reaching for the newest one is wrong for older dates — today's date confirmed the current (2026-01-01-onwards) version was correct here, but that check was necessary rather than assumed.
