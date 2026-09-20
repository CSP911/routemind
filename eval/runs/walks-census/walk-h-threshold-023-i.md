1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body

2. Answer
Sign-off: the division director.
Quotes: yes, three competing quotes are required.
(Delegation limit for this row is 20,011 thousand KRW; 11 working days to expect.)

3. Source
/v1/nodes/hard-threshold-legend-revision/body (confirmed current table applies for 2026-09-20)
/v1/nodes/hard-threshold-legend-category/body (laptops → category C1)
/v1/nodes/hard-threshold-legend-amount/body (~12 million won → amount V3)
/v1/nodes/hard-threshold-legend-term/body (until we cancel it → term M4)
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body (final answer)

4. Notes
The procurement table lists both a current threshold table (sec-hard-threshold, in force since 2026-01-01) and a superseded one (hard-threshold-v2, 2024-07-01 to 2025-12-31), plus an even older one. It would have been easy to grab hard-threshold-v2 by mistake since it appeared right above the current table in the listing. The legend-revision page made clear that for today's date (2026-09-20) the current table (three-qualifier index) is correct, so I used that.

The three qualifiers (category, amount, term) each needed their own legend lookup rather than guessing — the phrasing in the question ("a couple of laptops," "around 12 million won," "until we cancel it") maps directly to the legend tables' left-hand examples almost verbatim, so no interpolation was needed. No ambiguity in the final row lookup itself.
