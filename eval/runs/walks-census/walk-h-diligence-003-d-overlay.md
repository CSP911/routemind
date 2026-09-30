1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W1, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force from 2026-01-01 — likely holds the O1/W1/K4 row" --member /v1/nodes/hard-diligence-legend-revision/body "warns due diligence has three versions with different date ranges — need to confirm which version applies to today 2026-09-21" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, in case terms like site visit/review cycle are defined elsewhere"
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b0ebc6 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body

2. **Answer**
Site visit: no.
Re-review interval: every 36 months.

3. **Source**
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k4/body — in force from 2026-01-01 (current version; today is 2026-09-21, so no need to fall back to the superseded `hard-diligence-v2` or `supplier-due-diligence` versions).

4. **Notes**
Opening `/v1/nodes/sec-hard-diligence` as a member of the overlay expanded it into every origin/value/goods row in the current table, so the exact O1/W1/K4 row appeared directly without needing a separate lookup — the overlay's own table listing did the narrowing for me. Because I never explicitly added that row as a member (it just showed up when the parent table was opened), the close command reported it as "reached" rather than "used from a named member" — worth knowing that overlay bookkeeping distinguishes the two, though it didn't affect the answer.

The row document ends with a boilerplate "If the figures are exceeded" section about unapproved excess amounts and budget-holder approval — this reads like it was copy-pasted from an expense/threshold table and has nothing to do with site visits or re-review intervals. It's a red herring; ignored it in favor of the table fields (Site visit / Re-review interval) directly above.

I did not need to open `hard-diligence-legend-revision/body` or `sec-supplier-due-diligence` since the row's own footnote confirmed it is the current, in-force version for today's date.
