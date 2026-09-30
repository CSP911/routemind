1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Da Nang supplier, 8M KRW, made-to-spec: site visit required? file review frequency?" --member /v1/regions/procurement "procurement domain covers supplier approval thresholds and likely site visit / periodic review rules"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_63bf36 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body

2. **Answer**
No site visit is required. The supplier's file must be re-reviewed every 36 months.
(Also on this row, not asked but adjacent: screening score required is 79, financial statements are not required.)
This is from the current due-diligence table, in force from 2026-01-01 (today is 2026-09-20/21), for origin O4 (Da Nang) × value W1 (eight million won) × goods K2 (something made to our spec).

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body — maps "a supplier in Da Nang" to origin O4
/v1/nodes/hard-diligence-legend-value/body — maps "eight million won" to value W1
/v1/nodes/hard-diligence-legend-goods/body — maps "something made to our spec" to goods K2
/v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body — the row itself: site visit no, re-review interval every 36 months

4. **Notes**
The procurement region table immediately flagged that due diligence has three superseded versions (a `hard-diligence-legend-revision` warning row sits right next to the current and prior-version tables), so the first thing to check was which table is actually in force today. The row read confirmed it directly ("In force from 2026-01-01"), and today's date (2026-09-20/21) falls inside that window, so I didn't need to open the legend-revision or v2 documents separately — the row's own effective-date line was sufficient. It would have been easy to grab the superseded `hard-diligence-v2` table by mistake since it sits right next to the current one in the procurement listing with a similarly-worded description; the "SUPERSEDED" / "THE CURRENT ... TABLE" prefixes in the table listing are what saved that. All three legend inputs (origin, value, goods) matched an entry exactly — no nearest-value judgment calls were needed here.
