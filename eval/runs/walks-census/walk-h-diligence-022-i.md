1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body

2. **Answer**:
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Also: screening score required is 40, and financial statements for the last two years are required — given for context.)

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body (Daejeon = origin O1)
/v1/nodes/hard-diligence-legend-value/body (three hundred million won = value W3)
/v1/nodes/hard-diligence-legend-goods/body (people's time = goods K3)
/v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body (the answer: site visit yes, re-review every 12 months)

4. **Notes**:
The procurement area lists two due-diligence tables that look current at a glance: `sec-hard-diligence` (in force from 2026-01-01) and `hard-diligence-v2` (superseded, 2024-07-01 to 2025-12-31) plus a `supplier-due-diligence` page that turned out to be an overview of checks-before-registration (sanctions, code of conduct, disqualification screen), not the amount/site-visit table at all — it was a dead end I had to back out of. There's also a `hard-diligence-legend-revision` warning file flagging three versions of this table exist; I didn't need to open it because `sec-hard-diligence`'s own header already stated its effective date range and today's date (2026-09-20) falls inside it, but it would have been easy to grab the wrong version's row (`hard-diligence-v2` has its own similarly-shaped rows) if I hadn't checked the in-force dates first.

The three legends (origin, value, goods) each explicitly warn "if what you have is not listed, take the nearest entry above it" — none of that fuzziness was needed here since Daejeon, ₩300M, and "people's time" each matched a legend row exactly (O1, W3, K3), but it's a trap worth noting for similar questions with amounts or descriptions that don't land on an exact row.
