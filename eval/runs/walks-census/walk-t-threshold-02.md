1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/threshold-table/body

2. **Answer**
A purchase of 2,000,000 KRW net of VAT falls in the "500,000 – 3,000,000 KRW" band of the version of the approval threshold table in force in September 2023 (the oldest version, in force until 2024-07-01). It requires: **Division head, delegated** approval, with **2 quotes**.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (established which version covers 2023-09, i.e. the oldest one, at `threshold-table`)
- /v1/nodes/threshold-table/body (the actual figures used for the answer)

4. **Notes**
The procurement region's table only surfaces the two newer threshold versions directly (`hard-threshold-v2` for 2024-07-01 to 2025-12-31, and `sec-hard-threshold` as "current," from 2026-01-01). The oldest version — the one actually in force for a September 2023 date — isn't listed there at all; the legend-revision page names it only by its bare address (`threshold-table`), with no path. I had to find it by going sideways into `/v1/nodes/purchase-request` → `/v1/nodes/approval-threshold` → `/v1/nodes/threshold-table/body`, a different branch of the tree than the one the region table pointed at. If I had trusted the procurement region's listing alone and picked the "oldest-looking" of the two options shown there (`hard-threshold-v2`), I'd have given the 2024-07-01–2025-12-31 answer for a 2023 date — wrong version, and the exact trap the legend page warns about ("reaching for the newest is wrong for anything before 2026-01-01," but the *middle* one is just as wrong for 2023 as the current one is). The legend page's "one qualifier" description (amount only, no category/term) matched what `threshold-table` actually contained, which is what confirmed I had the right document.
