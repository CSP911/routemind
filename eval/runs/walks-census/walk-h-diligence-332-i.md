1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body

2. Answer

Yes, a site visit is required. The file is re-reviewed every 6 months.

(This is row origin O4 / value W4 / goods K3 of the current supplier due diligence table, in force from 2026-01-01, which covers today, 2026-09-20: Da Nang = origin O4, seven hundred million won = value W4, people's time = goods K3. That row also requires a screening score of 92 and audited financial statements for the last three years.)

3. Source

- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
- /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k3/body (site visit: yes; re-review interval: every 6 months)

4. Notes

- The first two documents I opened after finding the due-diligence area (/v1/nodes/sec-supplier-due-diligence/body and /v1/nodes/supplier-due-diligence/body) describe the due-diligence process in prose — sanctions/ownership, code of conduct, disqualification — but neither contains a site-visit answer or a re-review cadence. It would be easy to stop there and wrongly conclude due diligence is a one-time gate at onboarding (the overview page even flags that as "the one thing that goes wrong" — a trap the page itself names). The real per-supplier figures only live in the coded row table (sec-hard-diligence), reached by translating the three plain-language facts (location, value, goods type) through three separate legend pages.
- The procurement area table flagged that supplier due diligence has THREE historical versions with a legend-revision warning page. I didn't open that warning page directly, but the current table (sec-hard-diligence) states its own effective date (in force from 2026-01-01) and today is 2026-09-20, so the current table is the right one — no need to fall back to hard-diligence-v2 or the original supplier-due-diligence page for the figures.
- "People's time" mapping to goods K3 is not obvious from the phrase alone (it reads like it could mean labor/services, staffing, or consulting) — the legend confirms it's a distinct category from "something made to our spec" (K2), so it was worth checking explicitly rather than assuming.
