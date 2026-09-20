1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body

2. Answer
Site visit: no.
Re-review interval: every 36 months.
(For reference, this row also requires a screening score of 33, and financial statements are not required.)

3. Source
/v1/nodes/hard-diligence-legend-revision/body (confirms 2026-09-20 falls under the current, 2026-01-01-onward table, not the two superseded versions)
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body (the row with the actual figures)

4. Notes
The procurement area lists three separate due-diligence documents (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no date qualifier visible in the table listing itself — only the legend-revision page spells out which one is current. It would have been easy to grab the oldest or a wrong version by name-similarity alone; the legend page was the only thing that confirmed today's date (2026-09-20) maps to `sec-hard-diligence`, the three-qualifier current table. I did not need to open the origin/value/goods legend files themselves, since the question already gave the codes O1/W1/K4 directly and the row address was constructable by reading the printed table listing (not guessed) — the exact row `hard-diligence-row-origin-o1-value-w1-goods-k4` was present verbatim in the `sec-hard-diligence` table listing, so no separate legend lookup was needed to translate qualifiers into codes.
