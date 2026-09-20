1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/sanctions-ownership-checks/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body

2. Answer
No, a site visit is not required. The file is re-reviewed every 36 months.
(This is from the current supplier due-diligence table, in force since 2026-01-01, for origin O3 = Austin, value W1 = eight million won, goods K2 = something made to our spec.)

3. Source
/v1/nodes/hard-diligence-legend-origin/body (mapped "a vendor in Austin" → O3)
/v1/nodes/hard-diligence-legend-value/body (mapped "eight million won" → W1)
/v1/nodes/hard-diligence-legend-goods/body (mapped "something made to our spec" → K2)
/v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body (Site visit: no; Re-review interval: every 36 months)

4. Notes
- The procurement table warns that supplier due diligence has THREE versions with overlapping-looking names (hard-diligence-legend-revision). I didn't need to open that legend directly because /v1/nodes/sec-hard-diligence's own table header states it is "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01," and today is 2026-09-20, so it's current. Easy to grab the superseded `hard-diligence-v2` or `supplier-due-diligence` row instead if you don't check the effective dates — the addresses look similar and both were listed right next to the current one in the procurement table.
- I initially followed the "fourth page covering the ongoing side" lead in the sec-supplier-due-diligence overview into sanctions-ownership-checks, which does have its own re-run cadence ("Re-run the check annually for any vendor still active") — but that is the sanctions-screening cadence specifically, not the general vendor file re-review interval the question asked about. The actual answer to "how often does their file get looked at again" came from the origin/value/goods row table's "Re-review interval" field, not from that annual sanctions figure. Worth flagging because the two numbers (annual vs. every 36 months) answer different questions and are easy to conflate.
- All three legend lookups (Austin, eight million won, "something made to our spec") were exact matches in their tables, so no nearest-value judgment call was needed.
