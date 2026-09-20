1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body

2. Answer:
No site visit required. Re-review interval: every 24 months. (Also on file: screening score required 37, financial statements from last year.)

3. Source:
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body
(consulted for date-versioning check: /v1/nodes/hard-diligence-legend-revision/body)

4. Notes:
The procurement table lists three versions of the supplier due diligence subject (an old one, `hard-diligence-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-diligence` for 2026-01-01 onward), with an explicit warning that the oldest page says nothing about being superseded — reaching for it without checking dates would silently give a stale answer. Today's date (2026-09-20) falls under the current table, so that was the correct one to open. Since the question already gave origin/value/goods as codes (O1, W2, K4) rather than plain-language descriptions, the exact row was addressable directly from the current table's listing without needing the O/W/K legend files — those would only have been needed if the qualifiers had been described in prose instead of codes. The row's closing paragraph about "if the figures are exceeded" looks like boilerplate carried over from a different kind of row (thresholds/amounts) and doesn't actually apply to a site-visit/re-review row like this one — worth flagging as a documentation oddity, but it doesn't affect the two answers asked for.
