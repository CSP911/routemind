## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body

## Answer
No site visit is required. The file gets re-reviewed every 24 months.
(This is under the current due-diligence table, in force since 2026-01-01; today is 2026-09-20, so it applies.)

## Source
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body (Site visit: no; Re-review interval: every 24 months)

## Notes
- The procurement area table lists three parallel-looking things (`hard-diligence-legend-revision`, `hard-diligence-v2`, and `sec-hard-diligence`) plus a "where to start" overview page — it would be easy to open the superseded `hard-diligence-v2` table by mistake, since its row/label naming is presumably identical in shape. I stuck with `sec-hard-diligence`, whose own table description explicitly says it is "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01," which covers today's date, and the row itself restates that in-force date and points backward to the superseded versions — so I didn't need to open the legend-revision page at all.
- The "where to start" overview page (/v1/nodes/sec-supplier-due-diligence/body) was a bit of a detour — it describes four sub-pages (sanctions, code of conduct, disqualification triggers, and an "ongoing/re-run" page) but none of those is actually the row-level table with site-visit/re-review data. That data lives one level up, in the origin/value/goods row itself, not in any of the four "where to start" sub-pages. Worth noting so a future search doesn't waste time chasing that fourth page looking for the re-review interval.
- All three inputs (Austin, sixty million won, "just office consumables") matched a legend entry exactly, with no need to round to the nearest band — good, since the legends warn to round to the nearest entry and log the choice when there isn't an exact match, which would have needed calling out here.
