1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/corp-card
./bench/rmcli.py read /v1/nodes/corp-card/body
./bench/rmcli.py table /v1/nodes/card-limit
./bench/rmcli.py table /v1/nodes/entertainment
./bench/rmcli.py read /v1/nodes/entertainment-limit/body
./bench/rmcli.py table /v1/nodes/sec-entertainment-cases
./bench/rmcli.py read /v1/nodes/entertainment-meal-reclassified-internal/body
./bench/rmcli.py table /v1/nodes/sec-spending-that-needs-a-draft-first
./bench/rmcli.py read /v1/nodes/expense-draft-approval-overview/body
./bench/rmcli.py read /v1/nodes/expense-draft-approval-threshold-table/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body

2. Answer

Signature needed: the department head signs it off.
Other prices needed first: no — competing quotes required: none.

(This falls under the current approval threshold table, in force from 2026-01-01: category C4 = "dinner with a client", amount V1 = "about 700,000 won", term M4 = "until we cancel it". Delegation limit for this row is 1,051 thousand KRW, so 700,000 won is within it — no advance draft is needed for exceeding the limit, since it isn't exceeded.)

3. Source

/v1/nodes/hard-threshold-legend-revision/body (confirms the 2026-01-01 table is current for today's date)
/v1/nodes/hard-threshold-legend-category/body (maps "dinner with a client" to category C4)
/v1/nodes/hard-threshold-legend-amount/body (maps "about 700,000 won" to amount V1)
/v1/nodes/hard-threshold-legend-term/body (maps "until we cancel it" to term M4)
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body (the answer row: department head signs, no competing quotes)

4. Notes

The question's odd phrasing — "about 700,000 won" and "until we cancel it" — isn't loose wording, it's a direct quote of the exact row descriptors used in the procurement threshold legends (amount V1 and term M4, respectively). That's easy to miss going in: the first instinct is to treat "dinner with a client" as an entertainment-expense question (corporate card cap, per-head meal cap of 50,000 KRW, the worked case where a client cancels and the meal gets reclassified as an internal team meal with a 15,000 KRW/head cap). I went down that path first, read the entertainment cap page and the "meal that turned out internal" case in full, and neither answers "whose signature" or "quotes" at all — they're about spend caps and reclassification, not sign-off authority. The signature/quotes question is answered entirely by /v1/regions/procurement's current threshold table, not by /v1/regions/expense.

The near-miss risk here was stopping at the entertainment pages and answering from the 50,000-KRW-per-head cap logic, which has nothing to do with who signs or how many quotes are needed. Also worth flagging: "until we cancel it" superficially reads like it describes the client cancelling the dinner (matching the reclassification case), but in the threshold legend it's actually the term/duration qualifier ("until we cancel it" = an open-ended/ongoing commitment, term M4) — a different meaning of "cancel" entirely. Getting the category/amount/term legend lookups right depended on not assuming the entertainment-cap reading and instead checking the literal legend tables in procurement, which turned out to contain exact-match phrasing for all three inputs.

Also confirmed via hard-threshold-legend-revision that the 2026-01-01 current table (sec-hard-threshold) is the correct version for today's date (2026-09-21), not the superseded 2024-07-01–2025-12-31 version.
