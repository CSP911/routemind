1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body

2. Answer:
No site visit is required. The supplier's file is re-reviewed every 36 months.
(Also on this row, though not asked: screening score required is 31, financial statements not required.)

3. Source:
- /v1/nodes/hard-diligence-legend-revision/body (established that today's date, 2026-09-20, falls under the current 2026-01-01-onward table, not the two older versions)
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body ("something made to our spec" → goods K2)
- /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body (the answer: site visit no, re-review interval every 36 months)

4. Notes:
The subject has three superseded versions of the due-diligence rules (supplier-due-diligence, hard-diligence-v2, sec-hard-diligence), and the legend-revision page is explicit that reaching for the newest one is only correct if the question's date is 2026-01-01 or later — for a 2025-dated question the answer would have come from hard-diligence-v2 instead. Today being 2026-09-20 makes this one straightforward, but it would have been easy to skip that check and grab the current table by reflex regardless of date.

The bigger trap was upstream: /v1/regions/procurement lists a whole cluster of due-diligence pages (sec-supplier-due-diligence, supplier-due-diligence, disqualification-triggers, sanctions-ownership-checks, supplier-code-of-conduct) that describe the *qualitative* checks (sanctions screening, code of conduct, disqualification triggers) and read as if they might contain "site visit" or "review cadence" language. None of them do — those figures live only in the numeric legend/row table (sec-hard-diligence), keyed by origin/value/goods codes. It would be easy to stop at the narrative pages, conclude "not found," and miss the actual table that answers the question.

Mapping the three inputs to codes was mechanical (Daejeon=O1, 8M won=W1, "made to our spec"=K2) but each legend explicitly warns "if what you have is not listed, take the nearest entry" — none of that fuzziness was needed here since all three matched exactly, but it's a place a less exact question could go wrong.
