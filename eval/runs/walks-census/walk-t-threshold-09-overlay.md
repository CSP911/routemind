1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For something dated 29 June 2024 - two days before the first change - what was the delegation limit or who signed for a purchase of two million won net of VAT? Use version in force on that day." --member /v1/regions/procurement "approval threshold by amount for purchases, dated document"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py overlay add --id ov_2026-09-20_ef4a10 --address /v1/nodes/threshold-table/body --why "oldest approval threshold version, in force until 2024-07-01, covers 2024-06-29"
./bench/rmcli.py overlay add --id ov_2026-09-20_ef4a10 --address /v1/nodes/approval-threshold --why "table hosting threshold-table body, node reached from purchase-request"
./bench/rmcli.py read /v1/nodes/threshold-table/body
./bench/rmcli.py overlay close --id ov_2026-09-20_ef4a10 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-v2/body /v1/nodes/approval-threshold /v1/nodes/threshold-table/body

2. **Answer**:
2,000,000 KRW net of VAT falls in the "500,000 – 3,000,000 KRW" band. Approval: Division head, delegated. Quotes required: 2.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (establishes the three date ranges and that "until 2024-07-01" is the oldest version, at `threshold-table`)
/v1/nodes/hard-threshold-v2/body (confirms 2024-07-01 is the boundary date of "the first change," and that before it "the rule was the one in `threshold-table`")
/v1/nodes/approval-threshold (table node that resolves the bare name `threshold-table` to the address /v1/nodes/threshold-table/body)
/v1/nodes/threshold-table/body (the document actually answering the question — the pre-2024-07-01 approval threshold table)

4. **Notes**:
29 June 2024 is two days before 2024-07-01, which the legend-revision and v2 documents both name as the date the threshold rules changed — so the question wants the *oldest* of the three threshold versions, not the "v2" one that's prominently listed (and superseded-labeled) right in the procurement table. It would have been easy to grab /v1/nodes/hard-threshold-v2/body by pattern-matching "the non-current-labeled procurement threshold doc" without checking which side of 2024-07-01 the date falls on — the legend document exists specifically to catch that mistake, and its own text warns that "the oldest says nothing at all about having been replaced," i.e. the oldest document, /v1/nodes/threshold-table/body, has no internal marker telling you it's superseded. The other snag: the oldest version's address isn't listed anywhere in /v1/regions/procurement's own table — it only surfaces one hop further, from /v1/nodes/purchase-request → /v1/nodes/approval-threshold → /v1/nodes/threshold-table/body. Had I taken the legend document's bare mention of "`threshold-table`" at face value and typed /v1/nodes/threshold-table/body directly, that would have been constructing an address rather than using one printed by the tool, so I went back through the table chain to have it printed legitimately before reading it.
