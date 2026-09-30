1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W4, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods - likely has the answer" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of the diligence table; need to confirm which is in force today" --member /v1/nodes/sec-supplier-due-diligence "explains how the due-diligence pages fit together, may clarify site visit / review cadence terms"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b67f48 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row, for context: screening score required 76; financial statements — last three years, audited.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed the current table applies for a 2026 date)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body (the row with the answer)

4. **Notes**
The procurement area lists three generations of the supplier due diligence page (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend explicitly warns that the oldest version never says it was superseded — reaching for it without checking dates would silently give a stale answer. Today (2026-09-20/21) falls after the 2026-01-01 start of the current table, so `sec-hard-diligence`, indexed by all three qualifiers (origin, value, goods), was the right one; no ambiguity once the legend was read. The overlay's initial table listed the exact row address (origin-o3-value-w4-goods-k3) directly under the sec-hard-diligence member, so no further narrowing was needed — went straight from the working set to the row. One oddity: closing the overlay reported the row address as "reached" rather than "member," apparently because I cited the specific row's address in `--used` rather than the group header address I'd originally registered as the member (`sec-hard-diligence`) — cosmetic, didn't affect the answer.
