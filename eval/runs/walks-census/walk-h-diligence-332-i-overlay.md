1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Supplier in Da Nang, 700 million won, staffing/people's time category: is an on-site premises visit required, and how often is the supplier file re-reviewed?" --member /v1/regions/procurement "procurement table covers approval thresholds and likely vendor diligence rules by category/amount"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_001731 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body

2. **Answer**
Yes, a site visit is required. The supplier's file is re-reviewed every 6 months.
(Full row also lists: screening score required 92; financial statements — last three years, audited.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (established today's date, 2026-09-20, falls under the current version, not the two superseded ones)
/v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
/v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
/v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body (site visit: yes; re-review interval: every 6 months)

4. **Notes**
The subject has three versions of the same document (supplier-due-diligence, hard-diligence-v2, sec-hard-diligence), each in force for a different date range, and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version doesn't announce that it was superseded. Today's date (2026-09-20) falls after the 2026-01-01 start of the current table, so sec-hard-diligence was correct here — but this is clearly a trap for any question dated in 2025 or earlier, where grabbing the current table instead of hard-diligence-v2 would give a wrong answer. Worth double-checking the date every time this table is used.

Row lookup required decoding three separate legends (origin, value, goods) before the actual row address could be assembled — none of the plain-language terms ("Da Nang", "seven hundred million won", "people's time") appear directly in the row table; you have to translate through the legend tables first. No wrong turns otherwise; the path was linear once the legends were read.
