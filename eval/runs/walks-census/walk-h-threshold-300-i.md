1. **Commands**

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/corp-card
./bench/rmcli.py read /v1/nodes/corp-card/body
./bench/rmcli.py table /v1/nodes/sec-card-use-by-situation
./bench/rmcli.py read /v1/nodes/sec-card-use-by-situation/body
./bench/rmcli.py table /v1/nodes/sec-card-use-by-situation-1
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/card-limit
./bench/rmcli.py table /v1/nodes/entertainment
./bench/rmcli.py read /v1/nodes/entertainment/body
./bench/rmcli.py read /v1/nodes/entertainment-limit/body
./bench/rmcli.py read /v1/nodes/card-limit-table/body
./bench/rmcli.py table /v1/nodes/sec-spending-that-needs-a-draft-first
./bench/rmcli.py read /v1/nodes/expense-draft-approval-threshold-table/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body
```

2. **Answer**

The team lead signs it off, and no competing quotes are needed.

"Dinner with a client" is category C4, "about 700,000 won" is amount band V1, and "just the once" is term M1. The current threshold table (in force since 2026-01-01, which covers today, 2026-09-20) gives row C4/V1/M1: delegation limit 1,048,000 KRW, signed off by the team lead, competing quotes required: none, 2 working days to expect. 700,000 won is within that delegation limit, so nothing further is needed beyond the team lead's signature.

(Separately, the entertainment rule still applies regardless of who signs: the per-head meal cap is 50,000 KRW, qualifying evidence is mandatory above 30,000 KRW, and the attendee list — names and company — must be written on the receipt at the time or the whole claim is disallowed.)

3. **Source**

- /v1/nodes/hard-threshold-legend-category/body (maps "dinner with a client" → category C4)
- /v1/nodes/hard-threshold-legend-amount/body (maps "about 700,000 won" → amount V1)
- /v1/nodes/hard-threshold-legend-term/body (maps "just the once" → term M1)
- /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body (the answer: team lead signs, no quotes, 1,048,000 KRW delegation limit)
- /v1/nodes/hard-moved-threshold/body (confirms procurement's table, not approval's, governs thresholds for anything dated 2026-01-01 or later)
- /v1/nodes/entertainment/body and /v1/nodes/entertainment-limit/body (supporting: per-head cap and evidence rules that still apply on top of the signature/quote answer)

4. **Notes**

- The real trap was in `/v1/regions/approval`. It looks like the natural home for "whose signature do I need," and it has a `delegation-scope` table and its own thresholds — but `hard-moved-threshold/body` warns those are the pre-2026-01-01 rule. Since today is 2026-09-20, the live answer is only in procurement's `sec-hard-threshold`, not in approval at all. If I'd stopped at the first plausible-looking approval table I'd have given a superseded answer.
- I initially chased the corporate-card angle (card-limit-table, entertainment cap, draft-approval threshold table) expecting the "other prices" question to hinge on the card's per-transaction cap (300k/1M/3M by grade) or the generic draft threshold (drafts required above 1,000,000 KRW for a card transaction, 500,000 KRW for a PO without a quote on file). Both of those are real rules but they depend on facts the question doesn't give (the requester's grade) and neither is where the actual signer/quote answer lives for this case. The `sec-hard-threshold` category/amount/term table turned out to answer the question directly and unambiguously — "dinner with a client" and "about 700,000 won" and "just the once" are each given as literal worked examples in the legends, which made the row selection exact rather than a judgment call.
- The entertainment per-head cap (50,000 KRW/meal) is a real, still-binding constraint that this question doesn't ask about but that a claimant would trip over in practice — worth flagging even though it isn't part of the signature/quotes answer.
