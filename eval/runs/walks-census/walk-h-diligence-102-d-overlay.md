1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O2, value W1, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "customs/procurement risk classification with origin, value, goods codes and site-visit/review cadence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7437ef --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months.

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions applies to today's date)
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body (the row with the figures)

4. **Notes**
Supplier due diligence has three versions in force over different date ranges, and the oldest one gives no indication it was ever superseded — the legend-revision page warns explicitly that reaching for the newest table is wrong for any question dated before 2026-01-01. Today is 2026-09-20/21, so the current table (`sec-hard-diligence`, in force from 2026-01-01) is correct, but I checked the legend deliberately rather than assuming the top table listed was the right one — this is exactly the trap the page calls out. The row itself matched the three qualifiers (O2, W1, K3) exactly, no ambiguity there. The row's document also carries a boilerplate "If the figures are exceeded" section about expense claims and budget-holder approval that has nothing to do with site visits or review intervals — looks like leftover template text shared with an expense-report document type; I ignored it as not relevant to this question.
