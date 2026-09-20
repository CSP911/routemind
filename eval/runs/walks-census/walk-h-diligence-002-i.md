## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k3/body

## Answer
Site visit: no. Re-review interval: every 36 months.
(For reference: screening score required 32, financial statements not required.)

## Source
- /v1/nodes/hard-diligence-legend-revision/body
- /v1/nodes/hard-diligence-legend-origin/body
- /v1/nodes/hard-diligence-legend-value/body
- /v1/nodes/hard-diligence-legend-goods/body
- /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k3/body

## Notes
The procurement table lists three superseded/current versions of supplier due diligence (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20) falls under the current table, so this was a non-issue here, but it would have been easy to skip that check and silently use the wrong version — the warning specifically calls out 2025-dated questions as the trap case, which this wasn't, but the same trap applies in reverse if a question were backdated.

The three qualifiers (origin, value, goods) each have their own legend page that must be read before the row address can be built — the row addresses are literal (`origin-o1-value-w1-goods-k3`) and not guessable from the plain-language question, so all three legends had to be fetched. "People's time" mapping to goods category K3 (as opposed to K2, "something made to our spec") was the one genuinely ambiguous term in the question, but the legend's plain-language phrasing matched exactly, so no judgment call was needed.
