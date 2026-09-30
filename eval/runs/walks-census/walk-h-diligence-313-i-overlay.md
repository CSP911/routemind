1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Supplier in Da Nang, KRW 60,000,000, holds a licence: is an on-site visit required, and how often is the supplier file reviewed again?" --member /v1/regions/procurement "supplier diligence, site visits, and review cadence are procurement policy matters"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_1b56af --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body

2. **Answer**
No on-site visit is required. The supplier's file is re-reviewed every 24 months. (For completeness, the same row also sets: screening score required 85, financial statements for the last year.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirms which of the three due-diligence versions applies to today's date)
/v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
/v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
/v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
/v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body (the answering row: site visit no, re-review every 24 months)

4. **Notes**
Supplier due diligence has three versions of the same subject at different addresses (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that the oldest version never says it was superseded — reaching for it without checking the date would silently give the wrong row. Today (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-diligence`) was correct, but this is exactly the trap the page describes for a 2025-dated question, so it was worth confirming rather than assuming "current" was right by default.

The other near-miss: "a licence" isn't an obvious fit for any goods category until you actually read the goods legend — it maps to K4 exactly ("a licence"), so no interpretation was needed, but skipping the legend and guessing (e.g. assuming a licence counts as "people's time" or a service) would have picked the wrong row silently, since row addresses are built from codes with no cross-check.
