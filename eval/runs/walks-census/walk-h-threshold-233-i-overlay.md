1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Flights and hotels, about 40 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - need to find signature authority for ~40M won travel/open-ended term" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions - need to confirm which applies now" --member /v1/nodes/purchase-request "how many quotes needed before purchase"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d6994b --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m4/body

2. **Answer**: The CFO signs it. Yes — three competing quotes and a written comparison are required first. (Delegation limit 100,047 thousand KRW; 14 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m4/body

4. **Notes**: The three qualifiers had to be resolved independently before the row address could be built: "flights and hotels" → category C3, "about 40 million won" → amount V4, and "until we cancel it" → term M4 (the open-ended/no-fixed-end commitment, distinct from the one-off, annual-renewal, and three-year-lock terms). The revision-warning page was the thing that nearly caused a wrong answer — this subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the warning explicitly says reaching for the newest is wrong for dates before 2026-01-01. Since today is 2026-09-21, the current table (`sec-hard-threshold`, three qualifiers) is correct, but the check was necessary rather than assumed. No ambiguity remained once the three legends were read — the row address composed cleanly from C3/V4/M4.
