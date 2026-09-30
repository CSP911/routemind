1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W2, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force from 2026-01-01, likely holds the answer by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table, need to confirm which version applies for today's date 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_21f189 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body

2. **Answer**: No, a site visit is not required. The file is re-reviewed every 24 months.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions applies for a 2026-09-21 question — the current one, three-qualifier, in force since 2026-01-01)
- /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body (the actual row: Site visit = no, Re-review interval = every 24 months)

4. **Notes**: The procurement table lists three separate due-diligence tables (oldest, a 2024-07-01–2025-12-31 middle version, and the current one from 2026-01-01), all still present and none marked withdrawn. The legend-revision page explicitly warns that the oldest one "says nothing at all about having been replaced," so grabbing the first plausible-looking due-diligence page without checking dates would have silently produced a wrong or stale answer. Today's date (2026-09-21) put this squarely in the current table, but that only became certain after reading the revision legend — it wasn't obvious from the table listing alone, since /v1/nodes/sec-hard-diligence's row description just said "current" without stating the date range on the summary line I originally saw before opening the file. Also worth flagging: I never added the specific origin/value/goods row as an overlay member (only the parent table and the legend), yet the close command still accepted it as "used" and logged it as "reached ... from somewhere the overlay never named" rather than rejecting it — so overlay membership only needs the family of addresses you explored from, not every leaf you eventually read.
