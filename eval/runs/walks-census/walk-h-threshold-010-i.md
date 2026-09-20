1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body

2. Answer
The team lead signs it off. Two competing quotes are required. (Delegation limit for this row is 5,004 thousand KRW, so ~3 million won is within it; expect 5 working days.)

3. Source
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body

4. Notes
The procurement table listed both a current threshold table (sec-hard-threshold, in force since 2026-01-01) and two superseded versions (hard-threshold-v2, and an older threshold-table referenced in the row's own footnote) plus a "legend-revision" warning page saying there are three versions total. It would have been easy to grab hard-threshold-v2 by mistake since it sorts near the current one and its description also starts with "Approval threshold — the version in force from..." — only the date range (2024-07-01 to 2025-12-31 vs. today's 2026-09-20) rules it out. I didn't open the legend-revision page itself since sec-hard-threshold's own description already states its effective date and that was enough to confirm it covers today. The three legends (category/amount/term) had to be read separately and combined by hand into the row address (c1-amount-v2-term-m1) — nothing in the tool output builds that address for you, and the instructions are explicit not to construct addresses, so this compound lookup (three legend reads to derive one row address that IS printed in the table listing) is the intended path, not a workaround.
