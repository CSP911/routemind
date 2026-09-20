1. **Commands**

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-corporate-travel-agency
./bench/rmcli.py read /v1/nodes/expense-travel-agency-overview/body
./bench/rmcli.py table /v1/nodes/sec-spending-that-needs-a-draft-first
./bench/rmcli.py read /v1/nodes/expense-draft-approval-overview/body
./bench/rmcli.py read /v1/nodes/expense-draft-approval-threshold-table/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body
```

2. **Answer**

Signature: the team lead signs it off (the row's delegation limit is 5,036,000 KRW, so 3 million won falls within the team lead's authority — no one higher needs to sign).

Other prices first: yes — two competing quotes are required before this spend.

(Category = "flights and hotels" → C3; amount = "roughly 3 million won" → V2; term = "just the once" → M1.)

3. **Source**

- /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body — the row itself: signer, quote count, delegation limit
- /v1/nodes/hard-threshold-legend-category/body — maps "flights and hotels" to C3
- /v1/nodes/hard-threshold-legend-amount/body — maps "roughly 3 million won" to V2
- /v1/nodes/hard-threshold-legend-term/body — maps "just the once" to M1
- /v1/nodes/hard-moved-threshold/body — confirms spend-approval thresholds live in procurement (not approval) for anything dated on/after 2026-01-01, which today (2026-09-20) is

4. **Notes**

- Flights and hotels are covered as "travel expense" in the expense region, so I started there and nearly stopped at the wrong answer. The travel-agency overview (/v1/nodes/expense-travel-agency-overview/body) says a booking made through the agency "has already cleared the cap check" against fare/lodging caps, and the draft-approval threshold table (/v1/nodes/expense-draft-approval-threshold-table/body) has its own trigger — a single card transaction over 1,000,000 KRW needs a pre-approval draft. Both are real rules but neither is what the question is actually asking: they're about card-transaction caps and pre-approval drafts, not about "whose signature" and "how many quotes" for a purchase of this category/amount/term. I did not use either as the final source, only as a path I ruled out.
- The approval region looks like the obvious place for "whose signature do I need," but it explicitly warns that spend approval thresholds moved to procurement on 2026-01-01, and what's left in approval is the pre-2026 rule. Skipping that warning would have produced a stale answer.
- The current procurement threshold table (/v1/nodes/sec-hard-threshold) is a 64-row matrix addressed by three codes (category × amount × term) with no direct text search — the row address has to be built from three separate legend pages, not guessed. The question's own phrasing ("roughly 3 million won," "just the once") matches the legend tables' example wording almost verbatim, which is what made me confident this was the intended path rather than the travel-expense one.
- One thing I could not resolve with the tool: the travel-agency overview describes the agency itself comparing fares/rates against a cap, which sounds like it could double as the "quote" step — but nothing I found says whether that agency comparison counts as (or replaces) the "two competing quotes" required by the C3/V2/M1 row, or whether a separate quote has to be obtained and filed alongside the agency booking. I'm reporting the procurement row's requirement as written and flagging this gap rather than guessing.
