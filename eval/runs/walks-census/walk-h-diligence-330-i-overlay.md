1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Da Nang supplier, KRW 700,000,000, office consumables: on-site visit required? re-review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin/value/goods" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four diligence pages fit together" --member /v1/nodes/hard-diligence-legend-revision/body "warns diligence has three versions - need to confirm which is current for today's date"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3f6206 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also noted on the same row: screening score required 90, financial statements — last three years, audited.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body — confirms today's date (2026-09-20) falls under the current (2026-01-01 onward) diligence table, not either superseded version
/v1/nodes/hard-diligence-legend-origin/body — Da Nang maps to origin O4
/v1/nodes/hard-diligence-legend-value/body — seven hundred million won maps to value W4
/v1/nodes/hard-diligence-legend-goods/body — "just office consumables" maps to goods K1
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body — the row itself: Site visit = yes, Re-review interval = every 6 months

4. **Notes**
The current diligence table (sec-hard-diligence) is indexed by three separate qualifiers (origin, value, goods) each with its own legend page, and none of the rows repeat the plain-language descriptions — you must translate "Da Nang," "seven hundred million won," and "just office consumables" through the three legend tables before the row address can even be constructed correctly (it's printed by the table, so this is really about picking the right listed address, not building one). It would have been easy to grab the row for the wrong value band: 700 million won is the top-listed band (W4), and "office consumables" is explicitly the plain-language example given for K1, so this case maps cleanly onto the legends' own worked examples — but that also means it's exactly the kind of question a careless walk would rush through without checking the legends at all.

The bigger trap was the version warning. hard-diligence-legend-revision is explicit that this subject has three separate versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), that the oldest version says nothing about being superseded, and that reaching for "the newest" is wrong for anything dated before 2026-01-01. Today's date (2026-09-20) is safely inside the current version's range, so it wasn't a hard call here, but this is clearly the sharp edge of this question type — a question dated in 2025 would need hard-diligence-v2, not sec-hard-diligence, and nothing on the older pages would flag that you'd grabbed the wrong one.
