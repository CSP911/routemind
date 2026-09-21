1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon company, 700M KRW, office consumables: site visit required? review frequency?" --member /v1/regions/procurement "amount threshold and vendor diligence likely governed by procurement rules"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_ac0aba --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k1/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months. (This row also requires a screening score of 42 and audited financial statements for the last three years, though those weren't asked.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k1/body (site visit: yes; re-review interval: every 6 months)

4. **Notes**: The three qualifiers (origin, value, goods) each needed their own legend lookup before the row address could be assembled — none of the mappings are guessable (e.g. 700M won lands on W4, the top band, not an obvious "W3-ish" guess). The row's own header warns there are three versions of this table (`hard-diligence-legend-revision`), but the row I read states plainly it's "in force from 2026-01-01" with no end date, and today is 2026-09-20/21, so I didn't need to open the legend-revision or the superseded `hard-diligence-v2`/`supplier-due-diligence` versions — I just confirmed the in-force date against today rather than assuming "current table" meant current. Also worth flagging: the overlay's `close` reported all four addresses I used as "reached" rather than matches against named members, because I never formally `add`ed them to the working set (only the top-level procurement region was a member) — the answer is still correct, but the overlay hygiene was sloppier than it should have been.
