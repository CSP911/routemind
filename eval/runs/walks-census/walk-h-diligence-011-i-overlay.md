1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon vendor, 60M KRW, custom-spec goods: site visit required? file re-review frequency?" --member /v1/regions/procurement "vendor onsite verification and periodic vendor file review are procurement policy topics"
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c9284b --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body

2. **Answer**
No site visit is required. The vendor's file is re-reviewed every 24 months.
(Daejeon = origin O1, 60 million won = value W2, "something made to our spec" = goods K2. This row also gives: screening score required 35, financial statements from last year — not asked for but noted in case it's the next question.)

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body

4. **Notes**
The `sec-hard-diligence` table is indexed by three codes (origin/value/goods) that only make sense after reading the three legend files — the row addresses themselves give no hint which one applies, so skipping the legends would mean guessing among 64 rows. The legends translate plain language directly: "Daejeon" → O1, "sixty million won" → W2, "something made to our spec" → K2, so the mapping was unambiguous here, no nearest-match judgment call needed. The row's own header confirms `sec-hard-diligence` (in force from 2026-01-01) is current for today's date (2026-09-21), so there was no need to chase the `hard-diligence-legend-revision` warning about three historical versions — worth flagging that this table is a trap for anyone answering a diligence question without checking the effective date first. `overlay close` reported the four addresses as "reached" rather than "used" because I'd only added the top-level `/v1/regions/procurement` row as an overlay member and never formally added the legend/row addresses as members before closing — functionally the same outcome, but a stricter walk would have `add`ed each address to the working set as it was found.
