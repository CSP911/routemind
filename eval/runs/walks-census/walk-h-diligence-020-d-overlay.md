1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W3, goods K1, do we have to visit their premises, and how often is their file reviewed again?" --member /v1/nodes/sec-hard-diligence "current due diligence table by origin/value/goods, in force since 2026-01-01" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions with overlapping dates - need to confirm which applies today" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_08b276 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body

2. **Answer**:
Yes, a site visit is required. The file is re-reviewed every 12 months. (Also on the row: screening score required is 38, and financial statements for the last two years are required.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed the current, three-qualifier table applies to today's date, 2026-09-20/21, rather than the superseded v2 or oldest version)
- /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body (the actual figures: site visit yes, re-review every 12 months)

4. **Notes**:
The procurement region table listed three versions of supplier due diligence (oldest, a "v2" superseded 2024-07-01 to 2025-12-31, and the current one from 2026-01-01), each with a warning that the wrong one is easy to pick since none of them declare themselves superseded on their own page. I checked the legend-revision page before trusting the current table — it explicitly says "reaching for the newest is wrong for anything before 2026-01-01," which for this question (dated today, 2026-09-20/21) confirms the current three-qualifier table (`sec-hard-diligence`) is correct, but it's exactly the kind of check that's easy to skip since the current table's row also felt obviously right on its own. One odd but harmless note: I never explicitly `add`ed the row address (hard-diligence-row-origin-o1-value-w3-goods-k1/body) as an overlay member — it appeared automatically as a child row when I created the overlay against its parent table `sec-hard-diligence`. The close command flagged it as "reached" (used but not a named member) rather than a member, which is just a bookkeeping distinction, not an error.
