1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Dinner with a client, about 700,000 won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/corp-card "entertainment cap / client dinner spend likely covered here" --member /v1/nodes/sec-spending-that-needs-a-draft-first "over-cap spend / quotes-before-spend rules may live here"
./bench/rmcli.py table /v1/nodes/sec-card-use-by-situation
./bench/rmcli.py table /v1/nodes/sec-card-use-by-situation-1
./bench/rmcli.py overlay add --id ov_2026-09-21_d65af7 --address /v1/nodes/entertainment --why "exact match: entertaining a client, cap per head, evidence rules"
./bench/rmcli.py table /v1/nodes/entertainment
./bench/rmcli.py read /v1/nodes/entertainment-limit/body
./bench/rmcli.py table /v1/nodes/sec-entertainment-cases
./bench/rmcli.py read /v1/nodes/expense-draft-approval-threshold-table/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py overlay add --id ov_2026-09-21_d65af7 --address /v1/nodes/hard-moved-threshold/body --why "confirms current spend approval thresholds live in procurement (sec-hard-threshold), not approval, as of 2026-01-01"
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay add --id ov_2026-09-21_d65af7 --address /v1/nodes/sec-hard-threshold --why "current approval threshold table by category/amount/term since 2026-01-01"
./bench/rmcli.py overlay add --id ov_2026-09-21_d65af7 --address /v1/nodes/purchase-request --why "opens quotes requirement — how many quotes needed"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d65af7 --outcome answered --used /v1/nodes/hard-moved-threshold/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body

2. **Answer**
The team lead signs it off. No competing quotes are needed ("Competing quotes: none"). This is well within the delegation limit for this row (1,048,000 KRW), so there's no excess to escalate.

3. **Source**
/v1/nodes/hard-moved-threshold/body (confirms, for a 2026-09-20 date, the threshold now lives in procurement, not approval)
/v1/nodes/hard-threshold-legend-category/body ("dinner with a client" → category C4)
/v1/nodes/hard-threshold-legend-amount/body ("about 700,000 won" → amount V1)
/v1/nodes/hard-threshold-legend-term/body ("just the once" → term M1)
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body (the C4/V1/M1 row itself: team lead signs, no competing quotes, 1,048k KRW delegation limit)

4. **Notes**
The obvious first guess was wrong. "Dinner with a client" reads like an expense-region question (the region table even advertises "the entertainment cap" right there in its description), so I went down the expense/entertainment/corp-card path first and read the 50,000-KRW-per-head meal cap and the draft-approval threshold table (which has its own, unrelated "who signs" answer: team lead up to division head, keyed off card/PO/cash draft thresholds, not this question). None of that is what the question is actually asking — the entertainment cap page answers "how much can this cost," not "whose signature" or "do I need quotes."

The real turn came from the approval region: it has a loud warning page (hard-moved-threshold) saying spend-approval thresholds moved to procurement on 2026-01-01, and since today is 2026-09-20, the old approval-region rule (delegation-scope) is explicitly not the one to use. That's an easy trap — approval region matches the "whose signature" phrasing perfectly, and if I'd stopped at the first plausible-looking table there instead of reading the warning, I'd have cited a superseded rule.

The procurement threshold table (sec-hard-threshold) turned out to be keyed by three codes — category, amount band, term — each with its own legend table that translates plain-language phrasing directly into a code. All three phrases in the question ("dinner with a client", "about 700,000 won", "just the once") are literal example rows in those three legends, mapping cleanly to C4/V1/M1 with no interpolation needed. That precision was reassuring once found, but it wasn't obvious in advance that a restaurant dinner would be treated as a "procurement" category alongside laptops and consultants — nothing signals that up front; you only find it by reading the category legend itself.
