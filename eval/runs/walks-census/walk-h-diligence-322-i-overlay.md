1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Supplier in Da Nang, 300 million KRW, staffing/labor category: is an on-site premises visit required, and how often is the vendor file reviewed thereafter?" --member /v1/regions/procurement "procurement table covers approval thresholds by category/amount/term, likely includes vendor due diligence and site visit / review cadence rules"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_36ad67 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body

2. **Answer**
Yes, a site visit is required, and the file is re-reviewed every 12 months.
(Da Nang = origin O4, three hundred million won = value W3, "people's time" = goods K3 — an exact match on all three legends, no nearest-entry judgment call needed. Row O4/W3/K3 also requires a screening score of 88 and financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → O4)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → W3)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → K3)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body (site visit: yes; re-review interval: every 12 months)

4. **Notes**
The sec-hard-diligence table carries an explicit warning that supplier due diligence has three versions over time (`supplier-due-diligence`, then `hard-diligence-v2` from 2024-07-01, then the current table from 2026-01-01). I went straight for the current table (`sec-hard-diligence`) since today is 2026-09-21, which sits inside its "in force from 2026-01-01" window — but this is exactly the kind of question where picking the superseded `hard-diligence-v2` row instead would give a wrong, plausible-looking answer, since the row shapes are identical across versions. The row's own footer confirms the effective date, which is worth checking rather than trusting the table title alone. All three legend lookups (origin, value, goods) landed on exact matches ("a supplier in Da Nang", "three hundred million won", "people's time" are verbatim in the legend tables), so no ambiguity there — a cleaner case than the legends' own "nearest entry above it" fallback language implies is typical.
