1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W1, goods K1: premises visit required? review frequency?" --member /v1/nodes/sec-hard-diligence "listed as THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01" --member /v1/nodes/hard-diligence-legend-revision/body "warns diligence table has three versions - need to confirm which applies today" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_79c043 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body

2. **Answer**
No, a premises (site) visit is not required for origin O1, value W1, goods K1. The file gets re-reviewed every 36 months. (For reference, this row also requires a screening score of 30 and does not require financial statements.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions applies to today's date)
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body (the actual figures: Site visit = no, Re-review interval = every 36 months)

4. **Notes**
The procurement table lists THREE separate due-diligence pages by vintage (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and a legend-revision page warns explicitly that reaching for the newest one is wrong for any question dated before 2026-01-01, and that the oldest page says nothing about having been superseded — so guessing from the oldest page's silence would be a real trap. Today's date (2026-09-20 per the task instructions) falls after 2026-01-01, so the current table (`sec-hard-diligence`, indexed by three qualifiers: origin/value/goods) is the right one — this was worth confirming explicitly rather than assuming "current" was safe by default.

The row page's final section, "If the figures are exceeded," is boilerplate about excess claims and budget-holder sign-off that reads like it was copied from an expense/reimbursement page — it doesn't fit a due-diligence row (there's no "excess" concept for a screening score or a site-visit flag) and I did not use it in the answer.

The overlay tool logged the row address as "reached" rather than a named member, since I pulled it directly from the address printed under the `sec-hard-diligence` group heading in the overlay listing rather than issuing a separate `overlay add` for it. It didn't need to be added since it was already visible and correctly addressed in that same listing.
