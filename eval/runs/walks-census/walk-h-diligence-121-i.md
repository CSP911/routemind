## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body

## Answer
Yes, a site visit is required. The file is re-reviewed every 12 months.

(Stuttgart = origin O2, three hundred million won = value W3, "something made to our spec" = goods K2 — row origin-O2/value-W3/goods-K2 of the current supplier due diligence table, in force since 2026-01-01.)

## Source
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → O2)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → W3)
- /v1/nodes/hard-diligence-legend-goods/body (something made to our spec → K2)
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body (Site visit: yes; Re-review interval: every 12 months)

## Notes
- The `/v1/regions/procurement` table lists three parallel diligence pages: a legend-revision warning, a superseded `hard-diligence-v2`, and the current `sec-hard-diligence`. It would be easy to grab `hard-diligence-v2` by mistake since it sorts near the current table and isn't obviously dated in the listing text — had to open `sec-hard-diligence` specifically (marked "THE CURRENT... in force from 2026-01-01") and confirm today's date (2026-09-20) falls inside it before trusting the row.
- The "where to start" overview page (`sec-supplier-due-diligence/body`) reads like it should answer the question — it talks about ongoing/re-run checks — but it's prose about the process, not the actual numbers. The real figures only live in the leaf row file, one level further down than the overview suggests.
- All three legends carry the same fallback instruction ("if not listed, take the nearest entry above it") — not needed here since all three inputs (Stuttgart, 300M won, made-to-spec) matched an exact row in each legend, but worth flagging since a slightly different phrasing of the question could have required a judgment call.
