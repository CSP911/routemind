1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-corporate-travel-agency
./bench/rmcli.py read /v1/nodes/expense-travel-agency-overview/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body

2. **Answer**: The team lead signs it off. No competing quotes are needed (the row's "Competing quotes" field reads "none"). Delegation limit for this row is 1,032 thousand KRW, comfortably above the ~700,000 won in question, and 2 working days should be expected.

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body (maps "flights and hotels" → category C3)
/v1/nodes/hard-threshold-legend-amount/body (maps "about 700,000 won" → amount V1)
/v1/nodes/hard-threshold-legend-term/body (maps "just the once" → term M1)
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body (the answer: team lead, no competing quotes; current table, in force since 2026-01-01, applicable as of today 2026-09-21)

4. **Notes**: The expense region's corporate-travel-agency documents were a plausible-looking dead end — /v1/nodes/expense-travel-agency-overview/body says a booking through the agency "has already cleared the cap check," which reads as if it answers the signature/quotes question. But that page is about the fare/lodging *cap* (how much the company will pay), not the *approval threshold* (who signs and how many competing quotes are required) — a different concept living in the procurement region. It would have been easy to stop there and report "no signature needed, agency handles it," which is wrong. The real answer only surfaced by going to /v1/regions/procurement → sec-hard-threshold and discovering, via the category legend, that "flights and hotels" is explicitly category C3 in that table — confirming the procurement threshold table is the right and only place this is decided, despite living in a region whose one-line description talks about "buying something" rather than travel. Also had to actively check the amount legend and term legend before picking the row, since "about 700,000 won" and "just the once" are natural-language values that only make sense once translated to V1/M1 via those legend files — guessing the row address directly would have been wrong to attempt anyway, since addresses must come from what the tool prints. Finally confirmed the current table (2026-01-01 onward) was the applicable version given today's date, since the tool's own warnings flag three superseded versions of this threshold table.
