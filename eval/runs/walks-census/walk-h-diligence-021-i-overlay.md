1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon supplier, 300M KRW, custom spec item: site visit required? review frequency for their file?" --member /v1/regions/procurement "custom-spec supplier order, amount threshold, site visit and periodic review requirements likely live under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_26beba --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body

2. **Answer**
Yes, a site visit is required. The supplier's file is re-reviewed every 12 months.
(Also on the row, for context: screening score required 39; financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body — establishes that for a 2026-09-20 question, the current table (`sec-hard-diligence`, in force from 2026-01-01) is the right one, not the two older versions
- /v1/nodes/hard-diligence-legend-origin/body — Daejeon → origin O1
- /v1/nodes/hard-diligence-legend-value/body — three hundred million won → value W3
- /v1/nodes/hard-diligence-legend-goods/body — "something made to our spec" → goods K2
- /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body — the row itself: site visit yes, re-review interval every 12 months

4. **Notes**
- The legend-revision page is the load-bearing check here: this domain has three successive versions of the supplier due-diligence rules (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and it explicitly warns that the oldest version says nothing about being superseded — so grabbing the first "supplier due diligence" hit without checking dates would silently give a stale answer. Today's date (2026-09-20) falls in the current-table window, so `sec-hard-diligence` was correct, but this is exactly the kind of question where reaching for the newest-looking node without checking is not automatically safe (it happens to be right this time only because of the date).
- There's a decoy node, `/v1/nodes/sec-supplier-due-diligence`, an overview/navigation page that lists four sub-pages (sanctions/ownership checks, code of conduct, disqualification triggers, and an unnamed "ongoing" page) — none of which is the origin/value/goods table. It's a plausible-looking hit for "how often does their file get looked at again" (it even mentions "a fourth page covering the ongoing side... re-run rather than one-off"), but it doesn't actually contain the re-review interval; that's only on the specific coded row. Worth flagging since it's easy to stop there and report "not found on frequency" prematurely.
- The three qualifiers (origin, value, goods) each have their own legend page, and none of the row bodies repeat the human-readable inputs — you must translate through all three legends before fetching the row. All three mappings were exact matches to the phrasing in the question (Daejeon, three hundred million won, "something made to our spec"), so no ambiguity in that step.
- The overlay's `close` output flagged all five addresses I used as "reached = answered from somewhere the overlay never named" — I only ever added `/v1/regions/procurement` as a member and read everything else directly off the tables it surfaced, rather than formally adding each as an overlay member first. Functionally this didn't block the answer, but a more disciplined walk would add each address to the overlay as it's identified rather than fetching around it.
