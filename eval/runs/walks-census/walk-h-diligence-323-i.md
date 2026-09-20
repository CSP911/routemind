1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Full row also requires a screening score of 89 and financial statements for the last two years, if useful context.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body (answer: site visit = yes, re-review interval = every 12 months)

4. **Notes**
- The procurement table listed three due-diligence tables (`hard-diligence-v2`, `supplier-due-diligence`, and the current `sec-hard-diligence`), each explicitly flagged as superseded except the current one. It would be easy to grab the wrong version — the row address for `sec-hard-diligence` is dated "in force from 2026-01-01," which matches today's date (2026-09-20), so I used that one and ignored the older `hard-diligence-v2` and `supplier-due-diligence` pages.
- The three qualifiers (origin, value, goods) are only resolvable via their legend pages — the row itself doesn't restate what "O4/W3/K4" mean in plain language, so all three legends had to be fetched before the row address could even be identified with confidence.
- "A licence" mapping to goods category K4 is not obvious from the table's own name ("Which supply category a purchase belongs to") — had to read the legend's literal row text to confirm it wasn't, say, lumped in with "something made to our spec."
