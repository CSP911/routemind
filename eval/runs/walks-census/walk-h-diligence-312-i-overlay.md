1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Supplier in Da Nang, contract value 60,000,000 KRW (labor/services): is a premises site visit required, and how often is the supplier file reviewed thereafter?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, likely has site-visit and review-cycle rules by origin/value/goods type" --member /v1/nodes/sec-supplier-due-diligence "overview page tying the four due-diligence pages together, may clarify which page covers review cadence vs onboarding" --member /v1/nodes/hard-diligence-legend-revision "confirms which diligence table version is in force for today's date, 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_17fce7 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body

2. **Answer**
No site visit is required. The supplier's file is re-reviewed every 24 months. (For reference, this row also requires a screening score of 84 and last year's financial statements.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirms the current table, in force from 2026-01-01, governs a question dated 2026-09-21)
/v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
/v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
/v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
/v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body (the answering row: site visit no, re-review every 24 months)

4. **Notes**
The three qualifiers (origin, value, goods) each had to be looked up in a separate legend page before the actual row address could even be constructed — the table listing under /v1/regions/procurement only shows the raw origin/value/goods-coded row addresses, not anything indexed by plain-English terms like "Da Nang" or "people's time." Skipping any one of the three legends would have made it impossible to pick the right row out of the 64 listed.

The trickiest part was the currency/geography mismatch in the question: a supplier "in Da Nang" (Vietnam) priced "in won" (Korean currency). Nothing in the legends flagged this as invalid or asked for a conversion — the value legend is denominated in won regardless of the supplier's location, so I took the figures at face value (Da Nang for origin, sixty million won for value) rather than trying to convert currencies or treat the combination as an error. Worth flagging back to the asker if the currency was a typo, but RouteMind gave no basis to second-guess it.

Also worth noting: the diligence-legend-revision page warns hard about three superseded versions of this table and singles out 2025-dated questions as the trap case. Today's date (2026-09-21) falls cleanly after the 2026-01-01 cutover, so the current three-qualifier table (`sec-hard-diligence`) was the right one — but it would have been easy to grab the older `hard-diligence-v2` table by reflex if I hadn't checked the revision page first.

Finally, the overlay close output labeled all five addresses I used as "reached" rather than a clean match against overlay members — because the overlay was seeded with the table/section addresses (sec-hard-diligence, sec-supplier-due-diligence, hard-diligence-legend-revision) rather than the individual leaf pages the answer actually came from. This is expected given how the overlay explodes table members into their child rows, but it's worth knowing that "reached" here isn't a warning sign, just a byproduct of naming a table as a member instead of the specific leaf page.
