1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months.
(A company in Daejeon = origin O1, eight million won = value W1, a licence = goods K4.)

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body

4. **Notes**
The procurement area lists both a current supplier due-diligence table (`sec-hard-diligence`, in force since 2026-01-01) and two superseded versions (`hard-diligence-v2`, `supplier-due-diligence`), plus a `hard-diligence-legend-revision` page warning there are three versions total. It would have been easy to grab the plain-named `supplier-due-diligence/body` page first since it reads as the canonical doc — I did read it early, but it turned out to be the pre-2026 onboarding-checks overview with no site-visit or re-review figures at all, not the versioned table. Today's date (2026-09-20) falls inside the current table's validity window, so no legend-revision check was actually needed once I confirmed I was looking at `sec-hard-diligence`, but the naming similarity between `supplier-due-diligence` and `sec-hard-diligence`/`hard-diligence-*` is the one place this walk could have gone wrong.

The three legends (origin, value, goods) each map plain-language descriptions to a code letter+number, and the row address is built by concatenating all three codes in a fixed order (origin-value-goods) — the mapping is only written once per legend and not repeated in the row list, so all three had to be read before the target row address could be identified.
