1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Full row, for context: screening score required 70; financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established today's date, 2026-09-20, falls under the current 2026-01-01-onwards table, not the two superseded ones)
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body (the answer: site visit yes, re-review every 12 months)

4. **Notes**
- This subject has three superseded/current versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) living side by side with no withdrawal markers on the old ones — the legend-revision page is explicit that the oldest page "says nothing at all about having been replaced." Skipping that check and reading the first due-diligence page found (`supplier-due-diligence`, the pre-2024-07-01 version) would have given a plausible-looking but wrong answer, since it has no site-visit/re-review fields at all (it's a narrative page about the three checks and hit-handling, not the parameterized table). Today's date (2026-09-20) puts this squarely on the current table, `sec-hard-diligence`.
- The "where to start" overview page (`sec-supplier-due-diligence/body`) and the pre-2024 `supplier-due-diligence/body` page both looked like strong candidates initially since they came up first in the procurement table, but neither one actually contains site-visit or re-review figures — those only exist in the row-level pages of the current three-qualifier table. Easy to stop one level too early here.
- All three qualifiers (Austin, 300 million won, office consumables) matched a legend row exactly, so no "nearest entry" judgment call was needed — worth flagging because the legends explicitly allow for approximation when there's no exact match, which is a place this walk could have gone wrong for a slightly different vendor profile.
