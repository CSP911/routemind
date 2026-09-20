# Walk h-diligence-302-i

## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/nodes/sec-hard-diligence (wrong turn: went via /v1/nodes/sec-supplier-due-diligence and /v1/nodes/sec-supplier-due-diligence/body first)
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body

Full sequence actually run, in order:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body

## Answer
No site visit is required. The file is re-reviewed every 36 months.

(Full row for this case — Da Nang supplier, 8,000,000 won, "people's time" service — origin O4, value W1, goods K3: screening score required 80, financial statements not required, site visit: no, re-review interval: every 36 months. This is the table in force from 2026-01-01, current as of today, 2026-09-20.)

## Source
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → O4)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → W1)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → K3)
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body (site visit: no; re-review interval: every 36 months)

## Notes
- The procurement region table lists both a due-diligence "where to start" overview page (`sec-supplier-due-diligence`, four pages about onboarding checks: sanctions, code of conduct, disqualification triggers, and ongoing re-checks) and the actual current hard-numbers table (`sec-hard-diligence`). I opened the overview first, thinking "people's time" and "how often reviewed" might live in the ongoing-recheck narrative page — it doesn't have numbers, just describes the general policy that due diligence is not a one-time gate. That page was a dead end for this specific figure; the real answer is a per-row fact in the coded table, not prose.
- The region table's warning that "supplier due diligence has THREE versions" (a legend-revision page, `hard-diligence-v2` superseded 2024-07-01 to 2025-12-31, and an even older `supplier-due-diligence`) is a trap for anyone not checking today's date against the in-force window. `sec-hard-diligence` is explicitly labeled current since 2026-01-01, and today is 2026-09-20, so no need to open the legend-revision or older-version pages — but it would be easy to grab a row from `hard-diligence-v2` by accident since its address is very similar and it also has full row detail.
- The value legend maps "eight million won" to W1 as an exact match, not an approximation — worth flagging only because the legend's fallback instruction ("if not listed, take the nearest entry") suggested I should double check it wasn't a nearest-match guess. It's exact.
- "People's time" is the legend's literal wording for K3 (a services/labour category) — exact match to the question's phrase, so no interpretation needed there either.
