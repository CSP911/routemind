1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Dinner with a client, about 40 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "amount + term based approval threshold table, likely governs signature needed" --member /v1/nodes/purchase-request "how many quotes needed before purchase" --member /v1/nodes/sec-team-spending-ceilings "entertainment/client dinner might be expense related, checking relevance"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m2/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_1f11e8 --address /v1/nodes/sec-team-spending-ceilings --why "entertainment ceiling section not relevant; question is about approval threshold, not annual team spend ceiling"
./bench/rmcli.py overlay close --id ov_2026-09-21_1f11e8 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m2/body

2. Answer:
Sign-off: the division director.
Competing quotes: yes — three competing quotes plus a written comparison are required before purchase.
Working days to expect: 12.
Delegation limit for this row: 100,061 thousand KRW (~100 million won), so the ~40 million won dinner falls within this division-director-level band.

3. Source (in order used):
/v1/nodes/hard-threshold-legend-category/body — maps "dinner with a client" to category C4
/v1/nodes/hard-threshold-legend-amount/body — maps "about 40 million won" to amount V4
/v1/nodes/hard-threshold-legend-term/body — maps "renewing every year" to term M2
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m2/body — the row itself: signer, quotes, working days

4. Notes:
The phrasing "dinner with a client, about 40 million won, renewing every year" reads like a one-off client entertainment expense, which pulled me toward the expense region first (entertainment cap, team spending ceilings). But none of those expense-region tables answer "whose signature" or "how many quotes" — that's procurement/approval-threshold territory, keyed by category+amount+term, not by "is this a meal." The category legend turned out to have "dinner with a client" as a literal named row (C4), which resolved the ambiguity directly — I didn't have to guess or fall back to "nearest entry." Same for the amount (exact match to V4, ~40M) and term ("renewing every year" is the literal wording for M2). Nearly went wrong by treating this as an expense-report question instead of a procurement-threshold question; the giveaway was that "do I have to get other prices first" is a quotes/procurement concept, not an expense one. Also worth flagging: the procurement region separately lists a table at /v1/nodes/approval-threshold (under purchase-request) with a similar-sounding description ("Approval thresholds by amount"), but the procurement region table explicitly names /v1/nodes/sec-hard-threshold as "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01," so I used that one and left the other unopened — it looked like it could be an older or amount-only version and using it instead could have given a wrong or incomplete row (it doesn't appear to key by category/term).
