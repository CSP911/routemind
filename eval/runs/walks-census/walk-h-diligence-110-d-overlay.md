1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O2, value W2, goods K1, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, likely has the answer by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns there are three versions of this table with different date ranges - need to confirm which is current for today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_88729e --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body

2. **Answer**
No, a site visit is not required. The file (screening) is re-reviewed every 24 months.
(For completeness, this row also requires a screening score of 50 and last year's financial statements.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three table versions applies to a 2026-09-21 question)
- /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body (the actual answer: Site visit = no, Re-review interval = every 24 months)

4. **Notes**
Opening the overlay for the current table (`sec-hard-diligence`) immediately expanded into all 64 origin×value×goods row files, including the exact one needed (origin-o2-value-w2-goods-k1) — so the working set already contained the answer before any narrowing was done. The real risk here was the version trap: procurement has three superseded/current versions of "supplier due diligence" (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend page explicitly warns the oldest version says nothing about being replaced, so grabbing the first plausible-looking row without checking dates would silently give a stale answer. Reading the legend first (before trusting the row) confirmed 2026-09-21 falls under the current table (`sec-hard-diligence`), which matched the row already picked. Also worth noting: when closing the overlay, the row address was reported as "reached" rather than a matched member, because it was never added as its own explicit --member (it only appeared as a child row under the sec-hard-diligence table member) — the close still succeeded and recorded it correctly.
