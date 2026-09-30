1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Austin vendor, 60M KRW, licence: onsite premises visit required? how often is vendor file reviewed again?" --member /v1/regions/procurement "vendor diligence, site visits, and periodic re-review frequency would be under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c017a6 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body

2. **Answer**
No, no site visit is required. The vendor's file must be re-reviewed every 24 months.
(This is for a vendor in Austin (origin O3), a contract of sixty million won (value W2), and a licence (goods K4), under the current supplier due diligence table in force from 2026-01-01.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body — confirmed which of the three due-diligence table versions applies for today's date (2026-09-21 falls under the current, 2026-01-01-onwards version)
/v1/nodes/hard-diligence-legend-origin/body — mapped "a vendor in Austin" to origin O3
/v1/nodes/hard-diligence-legend-value/body — mapped "sixty million won" to value W2
/v1/nodes/hard-diligence-legend-goods/body — mapped "a licence" to goods K4
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body — the row giving "Site visit: no" and "Re-review interval: every 24 months"

4. **Notes**
The one place I nearly went wrong was the version question: supplier due diligence has three versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being superseded — so grabbing the first search hit without checking that page could silently give a stale answer. Today's date (2026-09-21) is safely inside the current table's range, so no ambiguity there, but it was worth checking explicitly rather than assuming "current" was the right pick. The three qualifiers (origin/value/goods) all mapped cleanly onto exact or near-exact legend entries — Austin, sixty million won, and "a licence" are each named verbatim or near-verbatim in their respective legends — so no judgment calls were needed on banding.
