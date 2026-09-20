## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/regions/expense
    ./bench/rmcli.py table /v1/nodes/corp-card
    ./bench/rmcli.py read /v1/nodes/expense-overview/body
    ./bench/rmcli.py table /v1/nodes/card-limit
    ./bench/rmcli.py table /v1/nodes/entertainment
    ./bench/rmcli.py read /v1/nodes/entertainment/body
    ./bench/rmcli.py read /v1/nodes/entertainment-limit/body
    ./bench/rmcli.py table /v1/regions/procurement
    ./bench/rmcli.py read /v1/nodes/procurement-overview/body
    ./bench/rmcli.py table /v1/nodes/purchase-request
    ./bench/rmcli.py table /v1/nodes/approval-threshold
    ./bench/rmcli.py read /v1/nodes/approval-threshold/body
    ./bench/rmcli.py read /v1/nodes/threshold-table/body
    ./bench/rmcli.py table /v1/nodes/sec-hard-threshold
    ./bench/rmcli.py read /v1/nodes/sec-hard-threshold/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

## Answer

The department head signs it off. Yes — three competing quotes are needed.

A ~12 million won client dinner is far over the card's per-transaction and entertainment caps
(entertainment meal cap is 50,000 KRW per head), so it has to go through Purchasing as a purchase
request rather than the corporate card. Under the current approval-threshold table (in force
since 2026-01-01), "dinner with a client" is category C4, "around 12 million won" is amount band
V3, and "just the once" is term M1. That row (C4/V3/M1) says: signs it off — the department head;
competing quotes — three; delegation limit 20,056 thousand KRW; 8 working days to expect.

## Source

- /v1/nodes/entertainment/body — establishes that an over-cap client dinner needs a purchase request like any other purchase
- /v1/nodes/entertainment-limit/body — the per-head entertainment caps that 12M won blows through
- /v1/nodes/procurement-overview/body — the fixed order (register vendor → quotes → approval → order)
- /v1/nodes/hard-threshold-legend-category/body — "dinner with a client" → category C4
- /v1/nodes/hard-threshold-legend-amount/body — "around 12 million won" → amount V3
- /v1/nodes/hard-threshold-legend-term/body — "just the once" → term M1
- /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body — the answer: department head signs, three quotes
- /v1/nodes/hard-threshold-legend-revision/body — confirms this current table is the one that applies for a 2026-09-20 question

## Notes

The walk nearly went wrong twice.

First, on the Expense side, it would have been easy to stop at "Entertainment" and answer straight
from its 50,000 KRW/head cap and "advance approval" language without ever naming who approves or
that quotes are involved — that page deliberately punts to Purchasing ("a client dinner over your
transaction cap needs a purchase request like anything else") rather than answering the question
itself.

Second, and more seriously: `/v1/regions/procurement` → `purchase-request` → `approval-threshold`
leads to a page (`threshold-table`) that *looks* like the complete, current answer — a clean
amount-only table with no warnings on the page itself, giving "10,000,000 KRW and over → CEO, with
a separate proposal, 3 quotes plus a comparison." That's wrong for today. The real current table
only turns up if you go back up to `/v1/regions/procurement` and separately open `sec-hard-threshold`,
which explicitly says it "replaces `threshold-table`." There's also a three-version warning file
(`hard-threshold-legend-revision`) that only appears in the region-level listing, not from the
`purchase-request` path — so the single-qualifier `threshold-table` route is a trap that gives a
plausible, confidently-formatted, and outdated answer (CEO instead of department head; the
category-specific row for a client dinner is materially different from the generic amount-only
row). The category/amount/term legend indirection (C4/V3/M1) is also easy to fumble — "around 12
million won" maps exactly to V3, but it would be easy to instead eyeball it against the old
generic table's "10,000,000 and over" band and never notice the two tables disagree.
