## Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/corp-card
./bench/rmcli.py read /v1/nodes/corp-card/body
./bench/rmcli.py table /v1/nodes/card-limit
./bench/rmcli.py table /v1/nodes/entertainment
./bench/rmcli.py read /v1/nodes/entertainment/body
./bench/rmcli.py read /v1/nodes/entertainment-limit/body
./bench/rmcli.py read /v1/nodes/card-limit-table/body
./bench/rmcli.py table /v1/nodes/sec-spending-that-needs-a-draft-first
./bench/rmcli.py read /v1/nodes/expense-draft-approval-overview/body
./bench/rmcli.py read /v1/nodes/expense-draft-approval-threshold-table/body
./bench/rmcli.py table /v1/nodes/sec-reimbursement-without-a-card
./bench/rmcli.py table /v1/nodes/sec-card-or-purchase-order
./bench/rmcli.py table /v1/nodes/sec-entertainment-cases
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/purchase-steps/body
./bench/rmcli.py read /v1/nodes/threshold-table/body
./bench/rmcli.py table /v1/nodes/sec-bands-and-quotes-in-practice
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/band-boundary-cases/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body

## Answer

The team lead signs it off. Yes — two competing quotes are required before the spend. (Delegation
limit on this row is 5,052,000 KRW; 5 working days to expect.)

This is the current, category-specific rule (in force since 2026-01-01): "dinner with a client" maps
to category C4, "roughly 3 million won" maps to amount band V2, and "just the once" maps to term M1.
The C4/V2/M1 row gives the signer and quote count directly — it does not track the generic amount-only
approval bands (which would have pointed to division head/CEO for this amount).

## Source

- /v1/nodes/entertainment/body — confirmed a client dinner over the card's per-transaction cap has to
  go through the same approval process as any other purchase, which is what sent the walk into
  Procurement rather than stopping at the card's entertainment cap.
- /v1/nodes/hard-threshold-legend-revision/body — established that /v1/nodes/threshold-table (found via
  Purchase request → Approval thresholds by amount) is the oldest of three versions, superseded twice,
  and that /v1/nodes/sec-hard-threshold is the one in force for a 2026 question.
- /v1/nodes/hard-threshold-legend-category/body — mapped "dinner with a client" to category C4.
- /v1/nodes/hard-threshold-legend-amount/body — mapped "roughly 3 million won" to amount V2.
- /v1/nodes/hard-threshold-legend-term/body — mapped "just the once" to term M1.
- /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body — the row itself: signer, quote
  count, delegation limit.

## Notes

The walk very nearly ended at the wrong table. Purchase request → "Approval thresholds by amount"
(/v1/nodes/threshold-table) answers fluently and plausibly for a 3,000,000 KRW purchase — it even has a
boundary-cases page (/v1/nodes/band-boundary-cases) that specifically resolves "exactly 3,000,000 KRW"
into the 3,000,000–10,000,000 band (CEO, 3 quotes). Nothing on that page or its neighbors says it is
outdated; the only place that says so is the legend-revision page in the procurement region root list,
one level up, and it's easy to never open it since /v1/nodes/threshold-table looks self-contained and
current on its own. Reading the procurement region table listing carefully — it names
/v1/nodes/sec-hard-threshold as "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01" and
flags that older pages are "still here and are superseded" — is what caught this before reporting the
CEO/3-quotes answer from the stale table.

Second near-miss: the expense region has its own, unrelated "draft required above 1,000,000 KRW"
threshold (/v1/nodes/expense-draft-approval-threshold-table) whose signer is "the same approver who
would sign a cash advance of the same size." That page is about getting ahead of a spend before it
happens and is a genuinely separate line from the procurement approval-threshold table — chasing it
down the cash-advance-approver trail would have produced a different, unrelated signer for the wrong
question ("do I need a draft" vs "who signs this purchase and how many quotes").

The current table (sec-hard-threshold) is indexed by three codes (category/amount/term) rather than a
simple amount band, and its three legend pages use almost the exact wording of the question ("dinner
with a client", "roughly 3 million won", "just the once") as the left-hand column — that phrasing match
is what confirmed this was the intended row rather than a coincidence, and it overrides the generic
amount-only banding: the category-specific delegation limit here (5,052,000 KRW) doesn't match any
boundary in the generic table, and the signer (team lead) is lower than what the generic band alone
would have implied for this amount.
