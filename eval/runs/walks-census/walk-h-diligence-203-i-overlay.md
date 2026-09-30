1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Austin vendor, licence, contract value 8,000,000 KRW: site visit required? re-diligence review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force from 2026-01-01" --member /v1/nodes/sec-supplier-due-diligence "overview of how the due diligence pages fit together" --member /v1/nodes/hard-diligence-legend-revision/body "warning about three versions of due diligence, need to confirm which applies to 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bbd1a9 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months.
(Full row also shows: screening score required 65, financial statements not required — not asked for but part of the same row.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body — confirms the current (three-qualifier) version applies to a 2026-09-20 question
- /v1/nodes/hard-diligence-legend-origin/body — maps "a vendor in Austin" to origin O3
- /v1/nodes/hard-diligence-legend-value/body — maps "eight million won" to value W1
- /v1/nodes/hard-diligence-legend-goods/body — maps "a licence" to goods K4
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body — the row itself, giving site visit: no, re-review interval: every 36 months

4. **Notes**
Supplier due diligence has three superseded/current versions indexed differently (one, two, then three qualifiers), and the legend-revision page explicitly warns that reaching for the newest is wrong for a pre-2026 date and that the oldest page never announces its own replacement. Today's date (2026-09-20) falls cleanly in the current version's range (2026-01-01 onwards), so this wasn't actually a trap for this question — but it's the kind of question where skipping that check would go unnoticed until a pre-2026 question hit the same overlay pattern. The three legend tables (origin, value, goods) are each "the only place the mapping is written down" and explicitly say the row indexes don't repeat the plain-language terms — so there's no way to guess the row address (e.g. o3-w1-k4) without reading all three legends first; I did that before touching a row address, which avoided constructing a wrong one. No ambiguity in the mapping itself: Austin → O3, eight million won → W1 exactly, "a licence" → K4 exactly — all direct matches, no nearest-entry judgment calls needed.
