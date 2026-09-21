1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon company, KRW 60,000,000, labor/staffing category: is an on-site visit required, and how often is the vendor file reviewed again?" --member /v1/regions/procurement "vendor diligence, site visit requirement, and review cadence by category/amount/region are procurement's domain"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3b3634 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k3/body

2. **Answer**: No, a site visit is not required. The vendor file is re-reviewed every 24 months. (Also on this row: screening score required is 36, and financial statements from the last year are needed.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established that today, 2026-09-20, falls under the current table, not either superseded version)
- /v1/nodes/hard-diligence-legend-origin/body (a company in Daejeon → origin O1)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
- /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k3/body (the row itself: site visit no, re-review every 24 months)

4. **Notes**: The main trap here is the three-versions warning on hard-diligence-legend-revision — the table has been rewritten twice, and reaching for whatever is newest without checking the question's date would be wrong for a 2025-dated question (that one needs `hard-diligence-v2`, not the current `sec-hard-diligence`). Since this question is being answered today (2026-09-20), the current table applies, but I made a point of reading the revision-legend first rather than assuming. The other easy slip is on the value legend: "sixty million won" doesn't sit at either end of the banding (8M / 60M / 300M / 700M) so it's tempting to eyeball it as "somewhere in the middle," but it's actually named exactly — W2 — no interpolation needed. Same for "people's time," which isn't an obvious label match until you see it listed verbatim as K3 (as opposed to something made to spec, K2, which is a plausible false read for a services engagement). All three qualifiers (origin, value, goods) had exact matches in their legends, so no nearest-entry judgment calls were needed.
