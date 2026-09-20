1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body

2. **Answer**: No, a site visit is not required. The file is re-reviewed every 24 months.
(Row: origin O4 = Da Nang, value W2 = sixty million won, goods K3 = people's time. Screening score required: 84. Financial statements: last year. This is the current version, in force from 2026-01-01, which covers today's date of 2026-09-20.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → O4)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → W2)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → K3)
- /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body (site visit: no; re-review interval: every 24 months)

4. **Notes**: The procurement area table flagged up front that supplier due diligence has three superseded versions with a legend-revision warning page (`hard-diligence-legend-revision`) and an older `hard-diligence-v2` (2024-07-01 to 2025-12-31) plus the original `supplier-due-diligence` prose page — easy to grab the wrong one. I didn't need to open the revision-legend separately because the matching row itself states its own force period (2026-01-01 onward) and today's date (2026-09-20) falls inside it, so the current `sec-hard-diligence` table was confirmed correct without a side trip. The bigger trap was the narrative page at `/v1/nodes/supplier-due-diligence/body` ("The three checks") and its sibling overview, which read like they'd answer the question but only describe the one-time onboarding gate (sanctions, code of conduct, disqualification screen) — no site-visit or re-review figures live there at all; those are only in the row-level table keyed by origin/value/goods. Also worth flagging: "sixty million won" matched a legend entry exactly (no rounding/nearest-band judgment needed), and "people's time" mapping to K3 (vs. K2 "something made to our spec") was the one place a wrong reading of the question could have changed the answer, since it's a service (labor/time) rather than a manufactured good.
