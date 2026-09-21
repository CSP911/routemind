1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Stuttgart supplier, KRW 60,000,000, office consumables: site visit required? review/reassessment frequency?" --member /v1/regions/procurement "approval threshold by category/amount/term row - likely covers vendor due diligence, site visits, periodic review"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2129bd --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body

2. **Answer**:
No site visit is required. The file gets re-reviewed every 24 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body

4. **Notes**:
This subject has three versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page is explicit that reaching for the newest is wrong for anything dated before 2026-01-01. Today (2026-09-20/21) falls after that date, so the current table `sec-hard-diligence` was the right pick — but this was a real branch point where a stale prompt date could have sent me to the wrong table entirely, and it was worth checking the revision legend before committing to a row rather than assuming "current" was safe. The initial overlay member I picked was `/v1/regions/procurement` (the top-level area), not the eventual current-table node itself — the region table then surfaced the due-diligence legend/version/table nodes directly, so the overlay's "reached" list ended up including addresses I never explicitly added as members, which the tool flags. That's expected behavior per the tool's own footer note, not an error. The three-qualifier lookup (origin/value/goods) via the three separate legend pages was straightforward once found, but it would be easy to skip one legend and guess a code wrong — each legend explicitly warns "this is the only place the mapping is written down," which is worth heeding literally.
