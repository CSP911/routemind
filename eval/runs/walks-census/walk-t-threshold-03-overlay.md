1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In January 2024, what was the delegation limit or who signed for a purchase of two million won net of VAT? Answer under the version of the approval threshold in force on that date." --member /v1/regions/procurement "approval threshold by category/amount/term lives here" --member /v1/regions/approval "approval chain and who can sign off lives here"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py overlay add --id ov_2026-09-20_70bb3e --address /v1/nodes/sec-approvals-that-move-money --why "likely nests delegation-scope and the oldest threshold-table referenced by hard-moved-threshold"
./bench/rmcli.py table /v1/nodes/sec-approvals-that-move-money
./bench/rmcli.py overlay remove --id ov_2026-09-20_70bb3e --address /v1/nodes/sec-approvals-that-move-money --why "no delegation-scope or threshold-table nested here"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py table /v1/nodes/sec-the-approval-behind-a-purchase
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py overlay add --id ov_2026-09-20_70bb3e --address /v1/nodes/purchase-request --why "nests approval-threshold, the by-amount-only table matching the oldest 'threshold-table' version"
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/threshold-table/body
./bench/rmcli.py overlay close --id ov_2026-09-20_70bb3e --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-v2/body /v1/nodes/purchase-request /v1/nodes/approval-threshold /v1/nodes/threshold-table/body

2. **Answer**:
For a purchase of 2,000,000 KRW net of VAT in January 2024, the amount falls in the band "500,000 – 3,000,000 KRW," which is signed by the **Division head, delegated** (2 competing quotes required). This is the pre-2024-07-01 version of the threshold, which is the one in force on the question's date — the delegation limit under this band runs from 500,000 up to 3,000,000 KRW net of VAT.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (established which of the three versions covers January 2024)
- /v1/nodes/hard-threshold-v2/body (confirmed the pre-2024-07-01 rule lives at `threshold-table`, not at this v2 page)
- /v1/nodes/purchase-request (table nesting the actual by-amount threshold table)
- /v1/nodes/approval-threshold (table nesting `threshold-table`)
- /v1/nodes/threshold-table/body (the actual pre-2024-07-01 threshold table used for the answer)

4. **Notes**:
The approval region's own listing is a trap for this question: `/v1/regions/approval` surfaces `hard-threshold-v2` and `sec-hard-threshold` directly under procurement, making it easy to grab the wrong version — sec-hard-threshold is current-only-since-2026, and hard-threshold-v2 explicitly covers 2024-07-01 to 2025-12-31, which does *not* include January 2024. Neither of those pages, nor the top-level procurement/approval table listings, ever print the oldest version's address directly — I had to read hard-threshold-v2's own body text, which states in prose "Before 2024-07-01 the rule was the one in `threshold-table`," and then hunt for where that id actually lived. It turned out nested two levels deep, under /v1/regions/procurement → /v1/nodes/purchase-request → /v1/nodes/approval-threshold → /v1/nodes/threshold-table/body — a path with no obvious signposting from the region tables. I also wasted one hop checking /v1/nodes/sec-approvals-that-move-money (in the approval region) on the theory that the old delegation/threshold rule had migrated there before the 2026 move to procurement; it held advance/emergency-spend pages but nothing about the base purchase threshold. The legend-revision page's warning that "the oldest says nothing at all about having been replaced" was accurate and worth heeding — threshold-table/body itself gives zero indication it's superseded, so trusting it in isolation (without first reading the legend-revision or v2 page) would have risked treating it as still current.
