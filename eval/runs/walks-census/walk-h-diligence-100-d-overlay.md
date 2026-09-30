1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O2, value W1, goods K1, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "procurement covers approval thresholds by category/amount/term - likely covers vendor diligence, site visits, review cadence by origin/value/goods"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_955eb8 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body

2. **Answer**:
Site visit: no. Re-review interval: every 36 months. (Screening score required: 46; financial statements not required — noted for completeness, not asked.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (established which of the three due-diligence versions applies for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body (the actual figures)

4. **Notes**:
This subject has three versions in force over different date ranges (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that the oldest version says nothing about being superseded — so grabbing the first "supplier due diligence" hit without checking dates would silently give stale figures. Today's date (2026-09-20) falls in the current-version range, so `sec-hard-diligence` was correct; had the question been dated in 2025 the answer would have had to come from `hard-diligence-v2` instead.

The matched row also carries a trailing "If the figures are exceeded" section about unapproved/unavoidable excess amounts and budget-holder sign-off — this reads like boilerplate from an expense/threshold-style template that doesn't fit a due-diligence checklist (site visit, screening score, re-review interval) and isn't responsive to what was asked, so it was not used as part of the answer.
