1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W4, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin/value/goods, in force since 2026-01-01" --member /v1/nodes/hard-diligence-legend-revision/body "warns diligence has three versions - need to confirm which applies today"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_865757 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months. (For reference, the same row also requires a screening score of 77 and audited financial statements for the last three years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions applies to today's date, 2026-09-21)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body (the actual figures)

4. **Notes**
Supplier due diligence has three superseded/current versions indexed by different numbers of qualifiers (one, two, three), and the legend page is explicit that reaching for the newest table is wrong for any question dated before 2026-01-01 — today's date (2026-09-21) falls in the current version's range, so `sec-hard-diligence` (three-qualifier, current) was correct, but this was worth checking rather than assuming since the trap is clearly intentional. The current table is organized as one row per origin/value/goods combination rather than as a single table body, so the O3/W4/K4 row was reachable directly by address from the /v1/regions/procurement listing without needing to open the parent sec-hard-diligence table itself. One oddity: closing the overlay reported the row address as "reached" rather than a named member, because it was only ever printed as a row under the sec-hard-diligence member, never added to the working set explicitly — worth adding rows explicitly in future if the overlay bookkeeping matters.
