1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A consultant's time, about 700,000 won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "one-time professional service purchase - approval threshold and quote requirement by amount/category"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8bcb47 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**
The team lead signs it off. No competing quotes are required (the row's "Competing quotes" field is "none"). Delegation limit for this row is 1,016 thousand KRW, and expect 2 working days.

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "about 700,000 won" → amount V1)
- /v1/nodes/hard-threshold-legend-term/body (mapped "just the once" → term M1)
- /v1/nodes/hard-threshold-legend-revision/body (confirmed the 2026-01-01-onward table is the one in force for today's date, 2026-09-20/21)
- /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body (the answering row: team lead, no competing quotes)

4. **Notes**
The approval-threshold table has three superseded versions in play (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), each indexed differently (one, two, and three qualifiers respectively), and the legend-revision page warns explicitly that "the oldest says nothing at all about having been replaced" — so it would be easy to land on a stale table and not notice. I deliberately opened `hard-threshold-legend-revision` last, after already reading the current row, just to double-check the 2026-01-01 table was still the right one for today's date rather than assuming the newest table (`sec-hard-threshold`) was automatically correct. It was — today's date is well past 2026-01-01 and there's no fourth, newer table.

The other easy misstep: the three legends (category/amount/term) are the *only* place the plain-English phrasing maps to the C/V/M codes used to index the 64 rows, and each legend explicitly says "this table is the only place the mapping is written down" — skipping any one of them means guessing which row to open. All three phrases in the question ("a consultant's time," "about 700,000 won," "just the once") happened to match legend rows exactly, so no nearest-entry judgment call was needed here.

The overlay's "reached" annotations (rather than a clean match) on close is just because those addresses were surfaced by drilling into `/v1/nodes/sec-hard-threshold`'s own table rather than being named directly as overlay members — not an error, just how the tool logs it.
