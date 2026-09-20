## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body

## Answer
The department head signs it off. No competing quotes are required ("Competing quotes: none"). This is under the delegation limit of 1,002 thousand KRW for this row (category C1 "a couple of laptops", amount V1 "about 700,000 won", term M3 "locked in for three years"). Expect about 4 working days.

## Source
- /v1/nodes/hard-threshold-legend-revision/body (confirms 2026-09-20 falls under the current, 2026-01-01-onwards table)
- /v1/nodes/hard-threshold-legend-category/body (maps "a couple of laptops" → C1)
- /v1/nodes/hard-threshold-legend-amount/body (maps "about 700,000 won" → V1)
- /v1/nodes/hard-threshold-legend-term/body (maps "locked in for three years" → M3)
- /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body (the answering row)

## Notes
The approval threshold table has three superseded versions covering different date ranges, and the legend-revision page explicitly warns that reaching for the newest version is wrong for anything dated before 2026-01-01. Today's date (2026-09-20) falls in the current version's range, so no correction was needed here, but this is an easy trap for a question dated earlier in 2025 or before mid-2024 — the middle version (`hard-threshold-v2`) would apply instead, and the oldest table gives no indication it was ever replaced. The row itself is only reachable by resolving all three qualifiers (category, amount band, term) independently through their own legend pages first — none of the plain-language terms in the question ("a couple of laptops," "700,000 won," "three years") appear directly in the row index, so skipping the legends would make it impossible to pick the right one of the 64 rows.
