1. Commands
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Da Nang supplier, 700M KRW, made-to-spec: site visit required? review cycle for supplier file?" --member /v1/regions/procurement "procurement region governs vendor/supplier diligence and review cadence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_352680 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body

2. Answer
Yes, a site visit is required. The supplier's file is re-reviewed every 6 months.
(Full row also requires: screening score of 91, audited financial statements for the last three years.)

3. Source
/v1/nodes/hard-diligence-legend-revision/body — confirmed which of the three versions of this subject applies to a 2026-09-21 question (the current one)
/v1/nodes/hard-diligence-legend-origin/body — Da Nang → origin O4
/v1/nodes/hard-diligence-legend-value/body — seven hundred million won → value W4
/v1/nodes/hard-diligence-legend-goods/body — "something made to our spec" → goods K2
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body — the row itself: site visit yes, re-review every 6 months

4. Notes
The trap here was the "three versions" warning on hard-diligence-legend-revision: there are three separate supplier-due-diligence documents (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and it explicitly says the oldest one doesn't admit having been superseded, so grabbing the first thing that looked right without checking the date would have silently given a wrong, out-of-force answer. Today (2026-09-21) is safely inside the current version's range, so sec-hard-diligence / hard-diligence-row-origin-o4-value-w4-goods-k2 was correct, but this is exactly the case the legend warns about for anyone answering from 2025.
The three qualifiers (origin/value/goods) each had their own legend page and none of them repeat the mapping elsewhere — "700 million won" and "Da Nang" and "made to our spec" only became O4/W4/K2 after reading all three legends, so skipping any one of them would have made it impossible to construct (not guess) the right row address.
