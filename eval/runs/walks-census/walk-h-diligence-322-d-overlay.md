1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O4, value W3, goods K3: is a premises visit required, and how often is the file reviewed?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, likely holds origin/value/goods matrix" --member /v1/nodes/hard-diligence-legend-revision/body "warns diligence table has three versions with different date ranges - need to confirm which version applies today"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9f718d --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(For context, the same row also requires a screening score of 88 and financial statements for the last two years, in force since 2026-01-01.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions applies to today's date)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body (the row with the answer)

4. **Notes**
The procurement area index flagged up front that due diligence has three versions covering different date ranges, with an explicit trap: "reaching for the newest is wrong for anything before 2026-01-01" and the oldest version "says nothing at all about having been replaced." I checked the legend-revision page before trusting the current table. Today (2026-09-20/21) is after 2026-01-01, so the current three-qualifier table (`sec-hard-diligence`, indexed by origin/value/goods as separate rows) is the right one, and the O4/W3/K3 address landed directly in it. Had the question been dated in 2025, the correct source would have been `hard-diligence-v2` instead — worth flagging since it's an easy trap to miss if you skip the legend page. Overlay closed as "answered" but noted the row was "reached" rather than a listed member, since I read it directly by its printed address rather than adding it to the working set first — the content and address are unaffected.
