1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Daejeon company, 700M won, licence: site visit required? review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, likely holds site visit and review frequency by origin/value/goods" --member /v1/nodes/sec-supplier-due-diligence "overview of how due diligence pages fit together, may clarify which table/column applies"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_83a588 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Full row also requires: screening score of 45, and audited financial statements for the last three years.)

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
/v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
/v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
/v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body (the row itself: site visit = yes, re-review interval = every 6 months)

4. **Notes**
The question's three clues (Daejeon, 700 million won, "a licence") only make sense once you find the three legend tables — they're not self-evident from the row filenames alone, and each legend is explicit that it is "the only place the mapping is written down," so guessing at the O/W/K codes without reading them would have been a real risk (e.g. assuming higher value bands or a different goods category by intuition). The procurement table listed three "hard-diligence" superseded/legend files up front (hard-diligence-v2, hard-diligence-legend-revision) that looked like they might be needed for version history, but the current table (sec-hard-diligence) is explicitly in force from 2026-01-01 and today is 2026-09-21, so no version check was actually needed beyond confirming the row cited that same in-force date, which it did. Also worth flagging: the overlay close command reported these four addresses as "reached" rather than the exact members I originally added to the working set (I'd only added the two parent tables, sec-hard-diligence and sec-supplier-due-diligence, as members — the actual leaf addresses used in --used were never formally added as members first). The tool accepted it anyway, but a stricter workflow would have added each leaf address to the overlay as I opened it.
