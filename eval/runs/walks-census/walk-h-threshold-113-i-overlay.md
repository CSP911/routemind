1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Consultant service ~3M KRW, open-ended until cancelled: whose signature, and quotes required?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - need signature authority" --member /v1/nodes/purchase-request "how many quotes are needed before purchase" --member /v1/nodes/hard-threshold-legend-revision/body "warns of 3 versions of threshold table, need to confirm which is current for today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_96c64e --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body

2. **Answer**
Signature: the division director signs it off.
Quotes: yes, two competing quotes are needed first.
(Delegation limit for this row is 5,023 thousand KRW; expect 8 working days.)

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "roughly 3 million won" → amount V2)
- /v1/nodes/hard-threshold-legend-term/body (mapped "until we cancel it" → term M4)
- /v1/nodes/hard-threshold-legend-revision/body (confirmed the current, three-qualifier table applies for a 2026 date)
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body (the matching row: division director, two quotes)

4. **Notes**
The procurement table is a matrix, not a single page — the question's three plain-English clauses ("consultant's time," "roughly 3 million won," "until we cancel it") each had to be run through a separate legend (category / amount / term) to get the C2/V2/M4 coordinates before the actual row could be addressed; guessing a row address directly would have been wrong. The revision-legend page was worth checking even though the current table was the obvious pick: it explicitly warns that reaching for the newest version is wrong for any date before 2026-01-01, and that the oldest version says nothing about being superseded — a trap for a differently-dated question, not this one, but worth verifying rather than assuming. Also note a one-day discrepancy between the task's stated "today" (2026-09-20) and the system's stated today (2026-09-21); both fall in the same 2026-01-01-onwards window so it didn't change which table version applies.
