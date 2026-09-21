1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W2, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "procurement table covers thresholds and likely vendor diligence by category/amount/term"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b7b8e1 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body

2. **Answer**: No, a site visit is not required. The file (re-review) is looked at again every 24 months. (For reference, the row also requires a screening score of 84 and last year's financial statements.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions applies to today's date)
- /v1/nodes/sec-hard-diligence (current table, in force from 2026-01-01, located the specific row)
- /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body (the answer: Site visit = no, Re-review interval = every 24 months)

4. **Notes**: The supplier due diligence subject has three versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) covering different date ranges, and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being superseded — so skipping that check could silently give an out-of-date answer. Today's date (2026-09-20/21) falls in the current table's range, so `sec-hard-diligence` was correct, but this was a deliberate check rather than an assumption. The row address itself directly matched the three qualifiers in the question (O4/W2/K3), so no legend lookups for origin/value/goods codes were needed — the question already gave the codes, not descriptions to translate.
