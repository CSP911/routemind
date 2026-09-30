1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Daejeon company, 8,000,000 KRW, licence (goods type?): site visit required? review/reassessment frequency?" --member /v1/nodes/sec-hard-diligence "current due-diligence table by origin/value/goods; likely has site visit requirement" --member /v1/nodes/sec-vendor-performance-and-renewal "renewal/reassessment cadence for vendor files" --member /v1/nodes/sec-supplier-due-diligence "overview of how the due-diligence pages fit together, in case site-visit and review live on different pages" --member /v1/nodes/hard-diligence-legend-revision "warns there are 3 versions of due diligence table; need to confirm which is current for today's date"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5a431e --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**
No, a site visit is not required. The file gets re-reviewed every 36 months.
(Full row context: screening score required 33, financial statements not required.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
- /v1/nodes/hard-diligence-legend-revision/body (confirms the three-qualifier table, in force 2026-01-01 onwards, is the one to use for today's date, 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body (the answering row: site visit "no", re-review interval "every 36 months")

4. **Notes**
- The three legends (origin/value/goods) are what actually let you build the row address — none of them repeat in the row list itself, so you have to open each legend before you can even name the file to read. It would be easy to guess a row address from intuition (e.g. assume Daejeon = domestic = O1 without checking) and get lucky, but the legend explicitly warns "never build one," so I read all three before touching the row.
- The bigger trap here is the revision legend. There are three versions of the due-diligence subject (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), each covering a different date range, and the revision-legend page is explicit that "reaching for the newest is wrong for anything before 2026-01-01." Today's date (2026-09-20) falls inside the current table's range (2026-01-01 onward), so `sec-hard-diligence` / the three-qualifier row was correct — but this is clearly the deliberate trap in this walk, and a question dated even a few months earlier would have needed `hard-diligence-v2` instead.
- Minor oddity: closing the overlay reported all five addresses I used as "reached = answered from somewhere the overlay never named," even though the legends and the target row are sub-files under `sec-hard-diligence`, one of my actual overlay members. This seems to be because the overlay member was the parent table address, not the specific leaf files — worth knowing that the tool tracks "used" at the exact address level, not by parent/child relationship, so it doesn't silently credit a member for its children.
