1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W2, goods K1: premises visit required? file review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions, need to confirm which applies today" --member /v1/nodes/sec-supplier-due-diligence "explains how the four due-diligence pages fit together"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9ae857 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 24 months.

3. **Source**
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body
/v1/nodes/hard-diligence-legend-revision/body (used to confirm the current, three-qualifier table applies to today's date, 2026-09-21)

4. **Notes**
This subject has three superseded versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the procurement table lists all three side by side with only short labels to tell them apart. It would have been easy to grab the wrong one, or to skip the date check entirely since the question gives no date of its own — I used today's date (2026-09-21), which falls under the current table (2026-01-01 onwards), so `sec-hard-diligence` was correct. The legend-revision page is explicit that the middle version applies for anything dated in 2025, which is exactly the mistake this walk was checking for. Opening `sec-hard-diligence` immediately surfaced the exact row for O3/W2/K1 (three qualifiers, matching the current table's indexing scheme), so no ambiguity remained once the version was confirmed.
