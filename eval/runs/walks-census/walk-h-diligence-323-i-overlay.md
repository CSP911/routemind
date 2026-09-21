1. Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Supplier in Da Nang, 300 million won, licence required - site visit needed? review frequency?" --member /v1/regions/procurement "supplier due diligence, site visits and review cadence would be under procurement"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py overlay add --id ov_2026-09-20_2aa938 --address /v1/nodes/hard-diligence-legend-origin/body --why "need origin code for Da Nang, Vietnam"
./bench/rmcli.py overlay add --id ov_2026-09-20_2aa938 --address /v1/nodes/hard-diligence-legend-value/body --why "need value band for 300 million won"
./bench/rmcli.py overlay add --id ov_2026-09-20_2aa938 --address /v1/nodes/hard-diligence-legend-goods/body --why "need goods code for a licence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py overlay add --id ov_2026-09-20_2aa938 --address /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body --why "the exact row: O4=Da Nang, W3=300M won, K4=a licence"
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2aa938 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body

2. Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.
(Full row: screening score required 89, financial statements for the last two years, site visit yes, re-review interval every 12 months.)

3. Source

- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3, exact match)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4, exact match)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body (the row itself: site visit yes, re-review every 12 months)

4. Notes

All three inputs (Da Nang, 300 million won, "a licence") matched a legend entry exactly, word for word — no nearest-neighbour banding was needed, so there was no ambiguity to record there.

The one place this could easily have gone wrong: the current diligence table (sec-hard-diligence) carries a loud warning that there are three historical versions (`supplier-due-diligence`, `hard-diligence-v2`, and the current one effective 2026-01-01). Today's date is 2026-09-21, which falls inside the current version's effective range, so I used the current table and did not need to open the superseded versions or the revision legend — but it would have been easy to grab the wrong version's row without checking the effective date first.

The regions table's one-line description for /v1/regions/procurement only mentions approval thresholds, not due diligence — the due-diligence tables turned out to be reachable from that same region row anyway, so it was still the right first pick, but the description alone undersold what was there.
