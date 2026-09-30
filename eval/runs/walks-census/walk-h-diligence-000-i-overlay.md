1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon vendor, 8M KRW, office consumables: site visit required? review frequency for vendor file?" --member /v1/regions/procurement "vendor due diligence, site visit and review frequency by category/amount likely live under procurement"
./bench/rmcli.py read /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5cde40 --outcome answered --used /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body

2. **Answer**:
No site visit is required. The vendor's file is re-reviewed every 36 months. (Screening score required: 30; financial statements not required.)

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body — mapped "a company in Daejeon" to origin O1
/v1/nodes/hard-diligence-legend-value/body — mapped "eight million won" to value W1
/v1/nodes/hard-diligence-legend-goods/body — mapped "just office consumables" to goods K1
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body — the row itself, with the figures

4. **Notes**:
The three qualifiers (origin, value, goods) mapped exactly onto the legend's example wording — "a company in Daejeon," "eight million won," "just office consumables" — with no rounding or nearest-match judgment needed, which is unusual and worth flagging in case that was deliberate on the question's part. The bigger risk was the table itself: `sec-hard-diligence`'s working set turned up two other supplier-due-diligence pages (`hard-diligence-legend-revision` and `hard-diligence-v2`) flagged as superseded, from a 2024-07-01–2025-12-31 version. It would be easy to grab a row from `hard-diligence-v2` by mistake since it uses the same origin/value/goods coding scheme — I confirmed I was reading the current table (`sec-hard-diligence`, in force from 2026-01-01, which the row's own footer also confirms) before trusting the row. Also note the row's "if the figures are exceeded" clause wasn't asked about but sits right below the answer — didn't include it since it doesn't answer the question asked.
