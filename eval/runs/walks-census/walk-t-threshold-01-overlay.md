1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In March 2023, what was the delegation limit or who signed for a purchase of two million won net of VAT? Answer under the version of the approval threshold that was in force on that date." --member /v1/regions/procurement "approval threshold by category, amount and term - likely holds delegation limits for purchases" --member /v1/regions/approval "approval chain / who signs off - could hold delegation of authority rules"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py overlay add --id ov_2026-09-20_ed002c --address /v1/nodes/purchase-request --why "led to approval-threshold sub-table, the oldest version path"
./bench/rmcli.py overlay add --id ov_2026-09-20_ed002c --address /v1/nodes/approval-threshold --why "container for the oldest threshold-table, in force pre-2024-07-01"
./bench/rmcli.py overlay add --id ov_2026-09-20_ed002c --address /v1/nodes/threshold-table/body --why "the actual oldest approval threshold document, in force in March 2023"
./bench/rmcli.py read /v1/nodes/threshold-table/body
./bench/rmcli.py table /v1/nodes/sec-approvals-that-move-money
./bench/rmcli.py overlay close --id ov_2026-09-20_ed002c --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/purchase-request /v1/nodes/approval-threshold /v1/nodes/threshold-table/body

2. **Answer**
Under the oldest version of the approval threshold (in force until 2024-07-01, so applicable to March 2023), a purchase of 2,000,000 KRW net of VAT falls in the 500,000–3,000,000 KRW band: approved by the **Division head, delegated**, requiring **2 quotes**.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (established which of the three versions was in force on the question's date)
/v1/nodes/purchase-request (led to the sub-table holding the oldest version)
/v1/nodes/approval-threshold (container node for the oldest threshold table)
/v1/nodes/threshold-table/body (the actual oldest approval-threshold table, used for the figures)

4. **Notes**
The approval-threshold subject has three versions layered in the same procurement region, and the two newer ones (`hard-threshold-v2` and `sec-hard-threshold`) are the ones that surface first and look most complete — it would have been easy to grab `hard-threshold-v2` since it's the only "threshold-v*" file directly listed in the procurement table and looks like a natural stop. The legend-revision page was the thing that saved me: it explicitly warns that the oldest version "says nothing at all about having been replaced," so nothing in the old document itself would have flagged that a newer one existed if I'd landed there without checking dates first.

The bigger snag: the oldest threshold table isn't reachable from the /v1/regions/procurement table at all — it's nested under /v1/nodes/purchase-request → /v1/nodes/approval-threshold → /v1/nodes/threshold-table/body, a path not shown anywhere in the procurement region's row list or its "why" text. The legend page names the address as `threshold-table` but gives no path, so I had to walk down through purchase-request to find it rather than construct the address. If I hadn't traced that path, the honest answer would have looked like "not found" for the pre-2024 version despite the newer two versions being sitting right there.

The oldest table's closing line ("The authority itself is set by the delegation rules — this table is that authority applied to purchasing") reads like it points to a separate delegation-of-authority document with a numeric "delegation limit" distinct from this band table. I checked /v1/regions/approval and /v1/nodes/sec-approvals-that-move-money for such a document but found only advance/expense-cap pages, nothing under a "delegation" heading — so I'm treating the band boundaries and approver named in threshold-table/body as the answer to both halves of the question (limit and signer) rather than holding out for a document that may not exist in this corpus.
