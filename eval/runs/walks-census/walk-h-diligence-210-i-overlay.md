1. Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Austin vendor, KRW 60M, office consumables: is a site visit required, and how often is the vendor file reviewed?" --member /v1/regions/procurement "procurement covers vendor approval thresholds, site visit requirements, and file review cadence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0e97ff --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body

2. Answer

No site visit is required. The vendor file is re-reviewed every 24 months. (Also on this row, for context: screening score required is 66, and financial statements from last year are needed.)

3. Source

- /v1/nodes/hard-diligence-legend-revision/body — established that today's date (2026-09-20) falls under the current version, `sec-hard-diligence` (in force from 2026-01-01), not the two older versions
- /v1/nodes/hard-diligence-legend-origin/body — mapped "a vendor in Austin" to origin O3
- /v1/nodes/hard-diligence-legend-value/body — mapped "sixty million won" to value W2
- /v1/nodes/hard-diligence-legend-goods/body — mapped "just office consumables" to goods K1
- /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body — the row itself: Site visit = no, Re-review interval = every 24 months

4. Notes

The table has three superseded/current versions of supplier due diligence with near-identical names (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that the oldest version says nothing about being replaced — so grabbing the first plausible hit without checking dates would have silently produced a 2024-vintage answer. Today's date (2026-09-20/21) put this squarely in the current version, but that had to be checked, not assumed.

The row lookup depends on three separate legend tables (origin, value, goods) that each map a plain-English phrase to a single-letter/number code, and the row address is only constructed by combining all three codes exactly (o3-value-w2-goods-k1) — get one wrong and you silently read a different vendor's rules. The wording in the question ("a vendor in austin", "sixty million won", "just office consumables") matched the legend wording closely enough that there was no ambiguity in this case, which made it easy to correctly resolve.

The overlay close command reported all five addresses as "reached" rather than "used" — worth flagging as slightly odd tool output, but the semantics (all were consulted and contributed) appear equivalent for this purpose. I did not need to touch approval-threshold tables (hard-threshold-*) since the question was only about site visits and file review cadence, both due-diligence topics, not approval routing.
