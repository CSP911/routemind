1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon vendor, 300M KRW, services (people's time): is a site visit required, and how often is the file reviewed again?" --member /v1/regions/procurement "procurement approval thresholds by category/amount/term likely cover site visit and review-cycle requirements"
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_ce569e --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Full row: screening score required 40, financial statements for the last two years, site visit yes, re-review interval every 12 months.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
- /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body (the answer: site visit yes, re-review every 12 months)

4. **Notes**
The three qualifiers (origin, value, goods) each needed their own legend lookup before the row address could be built — "three hundred million won" and "people's time" aren't self-evidently W3/K3 without reading the legends verbatim, and the legends explicitly warn they are the only place the mapping is written down, so I didn't try to guess it. The value matched an exact legend entry (three hundred million won = W3) rather than needing the "nearest entry" fallback, which was a relief since that fallback rule is easy to misapply.

One near-miss: /v1/nodes/sec-supplier-due-diligence (the "where to start" overview) mentions "a fourth page covering the ongoing side of the same checks, re-run rather than one-off" as one of four due-diligence pages, which could be mistaken for where re-review cadence lives. That page turned out to be irrelevant — the re-review interval is actually a column in the by-origin/value/goods row table (sec-hard-diligence), not a separate ongoing-checks page. Reading the overview first was useful for orientation but its four-page description didn't map cleanly onto where the actual answer sat.

Also noted but did not need: there are three historical versions of this table (a legend-revision warning flagged this). Today's date (2026-09-20/21) falls after the current table's 2026-01-01 effective date, so the current sec-hard-diligence/hard-diligence-row-... table applies; I did not check the superseded hard-diligence-v2 or original supplier-due-diligence versions since they don't govern today.

The overlay close command reported the four addresses I named as "reached ... from somewhere the overlay never named" — I had fetched them directly via read rather than adding them as overlay members first. Worth flagging as a minor workflow wrinkle: the overlay's own member list (procurement region + a handful of tables) never actually included the legend/row addresses that answered the question; I found them by drilling into sec-hard-diligence's entries list instead of adding each as a member. The answer is correct regardless, but the overlay's recorded working set undersells how I actually got there.
