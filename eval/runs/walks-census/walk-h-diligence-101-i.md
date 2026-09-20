1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/nodes/sec-hard-diligence (via /v1/regions/procurement)
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k2/body

2. Answer:
No, a site visit is not required. The supplier's file gets re-reviewed every 36 months.
(Also: screening score required is 47; financial statements not required.)

3. Source (in order used):
- /v1/nodes/sec-hard-diligence/body — confirms rows are indexed by origin/value/goods and that the re-review interval lives in the row
- /v1/nodes/hard-diligence-legend-origin/body — "a firm in Stuttgart" → origin O2
- /v1/nodes/hard-diligence-legend-value/body — "eight million won" → value W1
- /v1/nodes/hard-diligence-legend-goods/body — "something made to our spec" → goods K2
- /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k2/body — the answer row: site visit no, re-review every 36 months

4. Notes:
This walk went cleanly because all three qualifiers in the question ("Stuttgart", "eight million won", "something made to our spec") matched a legend row verbatim — no nearest-entry judgment call was needed, which is unusual and worth flagging in case that was the point of the phrasing. The one place I nearly went wrong: the procurement region table listed a `hard-diligence-legend-revision` node warning that due diligence has THREE versions (superseded `supplier-due-diligence`, superseded `hard-diligence-v2` covering 2024-07-01 to 2025-12-31, and the current `sec-hard-diligence` in force from 2026-01-01). I almost opened the legend-revision page to double check dates, but the row itself states its own effective date (2026-01-01) and today is 2026-09-20, so `sec-hard-diligence` is unambiguously current and I didn't need the revision-history page. Also worth noting: I went in through /v1/regions/procurement rather than /v1/nodes/sec-supplier-due-diligence (the "where to start" overview) — that overview page is about pre-registration checks (disqualification triggers, sanctions/ownership, code of conduct) and does not itself contain the site-visit/re-review figures, so it would have been a detour.
