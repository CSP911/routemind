1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W4, goods K4: site visit required? review frequency?" --member /v1/regions/procurement "goods/value/origin classification and vendor diligence likely under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_4b34ef --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body

2. **Answer**:
Yes, a site visit is required. The file is re-reviewed every 6 months.
(For context, this row also requires a screening score of 93 and audited financial statements for the last three years.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established which of the three versions applies for today's date, 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body (the answer: site visit = yes, re-review interval = every 6 months)

4. **Notes**:
Supplier due diligence has three historical versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that the oldest version never says it was superseded — reaching for the current table without checking the date would be silently wrong for older questions. For this question, today's date (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` is the right one — but I checked the revision-legend page first rather than assuming, since it was flagged as the one case worth being careful about. The row address itself was easy to find once the goods/origin/value table was open, since the three qualifiers (O4/W4/K4) map directly to the file name.
