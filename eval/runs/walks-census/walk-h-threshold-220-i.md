1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body

2. **Answer**
Flights and hotels map to category C3, "around 12 million won" maps to amount band V3, and "just the once" maps to term M1. For row C3/V3/M1 (current table, in force since 2026-01-01): the department head signs it off, and three competing quotes are required before approval. Delegation limit for this row is 20,040 thousand KRW; expect 8 working days.

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "flights and hotels" → C3)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "around 12 million won" → V3)
- /v1/nodes/hard-threshold-legend-term/body (mapped "just the once" → M1)
- /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body (the answer: signer, quotes required)

4. **Notes**
The initial /v1/regions listing's blurb for "expense" mentions per-diem and trip pay, which could tempt a search into the travel-expense/per-diem pages — but the actual question ("whose signature," "do I have to get other prices first") is an approval-threshold question, which lives under /v1/regions/procurement, not /v1/regions/expense. Almost went down the expense-region path first before recognizing the question was about sign-off authority and competing quotes, not reimbursement mechanics.

The three legend tables (category, amount, term) are the only place the plain-language phrases ("flights and hotels," "around 12 million won," "just the once") are translated into the row codes (C3, V3, M1) — the row filenames themselves give no hint which codes correspond to which real-world description, so skipping the legends would make it impossible to pick the right row out of 64.

Also worth flagging: there are three historical versions of this threshold table (current since 2026-01-01, a v2 from 2024-07-01–2025-12-31, and an older `threshold-table`). Today's date (2026-09-21 per the system clock, 2026-09-20 per the task prompt) falls under the current version either way, so this didn't change the answer, but it's the kind of date boundary that could easily bite on a different query date.
