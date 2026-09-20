## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k4/body

## Answer
Yes, a site visit is required. The file is re-reviewed every 12 months.

(Row context: Daejeon → origin O1, three hundred million won → value W3 exactly, a licence → goods K4. Screening score required: 41; financial statements: last two years.)

## Source
- /v1/nodes/hard-diligence-legend-origin/body (mapped "a company in Daejeon" → O1)
- /v1/nodes/hard-diligence-legend-value/body (mapped "three hundred million won" → W3)
- /v1/nodes/hard-diligence-legend-goods/body (mapped "a licence" → K4)
- /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k4/body (the answer: site visit yes, re-review every 12 months)

## Notes
- The region table for procurement lists both a current due-diligence table and older superseded ones (`hard-diligence-v2`, and a `hard-diligence-legend-revision` warning page). It would be easy to grab a stale row by accident. I stayed on `sec-hard-diligence`, which states it is "in force from 2026-01-01" — that covers today (2026-09-20) — and the row itself repeats that same in-force date, so I didn't need to open the legend-revision or v2 pages to be sure.
- The `/v1/regions/procurement` table has both `/v1/nodes/sec-supplier-due-diligence` ("where to start", a narrative overview of onboarding checks — sanctions, code of conduct, disqualification triggers) and `/v1/nodes/sec-hard-diligence` (the actual banded table by origin/value/goods). The first one reads like it could be the answer but it's onboarding-checklist prose with no site-visit or re-review figures — the real numbers are only in the banded table under `sec-hard-diligence`. Easy to stop one level too early.
- The value legend had an exact match (three hundred million won = W3 exactly), so no rounding/nearest-entry judgment call was needed there, unlike origin/goods which were also exact matches. No ambiguity in this walk once the three legends were read.
