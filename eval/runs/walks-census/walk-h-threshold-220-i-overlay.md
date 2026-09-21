## Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, around 12 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by amount and how many quotes are needed - matches signature and other prices" --member /v1/regions/expense "flights and hotels for a one-time trip is a business trip expense; may define its own approval/quoting rules"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c8888f --outcome answered --used /v1/regions/procurement /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body

## Answer

The department head signs it off. Yes — three competing quotes are required first.
(Delegation limit for this row is 20,040 thousand KRW, so 12 million won falls within it.)

## Source

- /v1/nodes/hard-threshold-legend-category/body — "flights and hotels" → category C3
- /v1/nodes/hard-threshold-legend-amount/body — "around 12 million won" → amount V3
- /v1/nodes/hard-threshold-legend-term/body — "just the once" → term M1
- /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body — the row itself: department head signs, three competing quotes, 8 working days to expect
- /v1/nodes/hard-threshold-legend-revision/body — confirms today's date (2026-09-21) falls under the current table (in force from 2026-01-01), not one of the two superseded versions

## Notes

The initial working set also pulled in /v1/regions/expense, guessing this might be a travel-expense question (per-diem, corporate card) rather than a procurement one. It wasn't needed — the question's own wording ("whose signature," "other prices first") is procurement-threshold language, and the expense-side pages never got touched.

The real trap was version drift, not category ambiguity. The threshold table exists in three superseded forms (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), each indexed differently (one/two/three qualifiers), and the older ones don't announce that they've been replaced. I deliberately checked the revision-legend page against today's date before trusting the row I read, rather than assuming "current" was safe — for a 2025-dated question the correct answer would have been the middle version instead.

Mapping "flights and hotels" / "around 12 million won" / "just the once" to C3/V3/M1 was a direct, unambiguous lookup — the three legend tables spell out exactly these example phrasings, so there was no real risk of miscoding the row.
