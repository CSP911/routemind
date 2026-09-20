# Walk h-threshold-201-i

## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2/body

## Answer
The team lead signs it off. No competing quotes are needed (none required).
Delegation limit for this row is 1033 thousand KRW, and 3 working days should be expected.
(Category C3 = flights and hotels, amount V1 = about 700,000 won, term M2 = renewing every year.)

## Source
- /v1/nodes/hard-threshold-legend-category/body
- /v1/nodes/hard-threshold-legend-amount/body
- /v1/nodes/hard-threshold-legend-term/body
- /v1/nodes/hard-threshold-legend-revision/body
- /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2/body

## Notes
The threshold table has three superseded/current versions (`threshold-table`, `hard-threshold-v2`,
`sec-hard-threshold`), and the legend-revision page is explicit that reaching for the newest one is
wrong for any question dated before 2026-01-01. Today's date (2026-09-21) falls cleanly in the
current table's range, so this wasn't actually ambiguous, but it's the kind of question where
skipping that check would have been a real mistake for a date in 2025. I made a point of reading
the revision legend before trusting `sec-hard-threshold` rather than assuming the current table
applied by default.

The three legends (category, amount, term) had to be resolved independently before the row address
could be built — there's no way to guess the row address from the plain-language question, and the
table explicitly warns never to construct one. "About 700,000 won" and "flights and hotels" and
"renewing every year" mapped cleanly onto single legend rows (C3, V1, M2) with no fuzzy-matching
needed, so no judgment calls were required there.
