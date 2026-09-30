1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O2, value W4, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force from 2026-01-01, likely holds the answer by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns there are three versions of this table with different date ranges; need to confirm which is current for today 2026-09-21" --member /v1/nodes/sec-supplier-due-diligence "overview of how the due-diligence pages fit together, may clarify terms like premises visit / file review cadence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_26f1f2 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body (the row itself, giving "Site visit: yes" and "Re-review interval: every 6 months")
/v1/nodes/hard-diligence-legend-revision/body (used to confirm today's date, 2026-09-21, falls in the 2026-01-01-onwards version, so `sec-hard-diligence`'s three-qualifier rows are the correct table and not the superseded `hard-diligence-v2` or `supplier-due-diligence`)

4. **Notes**
Opening /v1/nodes/procurement's table showed a WARNING that supplier due diligence has three versions covering different date ranges, with a legend-revision page for figuring out which applies. That was the near-miss: it would have been easy to jump straight to the current-looking `sec-hard-diligence` table without checking whether today's date actually falls under it. Reading the revision legend confirmed 2026-09-21 falls under the 2026-01-01-onwards version (three qualifiers: origin, value, goods), which matches the row address format used, so no correction was needed — but it was worth verifying rather than assuming "current" is always right, since the legend explicitly warns against that assumption for older dates.

One bookkeeping wrinkle: the overlay was created with `sec-hard-diligence` (the table) as a member, not the specific O2/W4/K3 row (a child of that table) or the legend-revision file, and the close command reported the row as "reached" (used but never named as a member) rather than "member." This didn't affect the answer, but it means the working set as declared didn't literally contain the address the answer came from — only its parent table.
