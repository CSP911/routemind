1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 24 months. (Also on this row: screening score required is 53, financial statements needed cover the last year.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
- /v1/nodes/hard-diligence-legend-revision/body (confirms today, 2026-09-20, falls under the current 2026-01-01-onwards table, not the two superseded versions)
- /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body (the answer: site visit = no, re-review interval = every 24 months)

4. **Notes**
- The procurement area lists supplier due diligence in three superseded/current versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), each indexed by a different number of qualifiers (one, two, three respectively). It would have been easy to grab the wrong version by just picking the top-looking match; the `hard-diligence-legend-revision` page exists specifically to force a date check, and it explicitly warns that the oldest version "says nothing at all about having been replaced" — so if you hit that page first without checking dates, you'd have no clue you were looking at retired guidance. Today's date (2026-09-20) is safely inside the current table's range (2026-01-01 onwards), so no ambiguity in the end, but this is the place I'd have gone wrong on a 2025-dated question.
- The three legend tables (origin, value, goods) had to be resolved independently before the row address could be built — "Stuttgart," "sixty million won," and "a licence" are exact matches in their respective legends, so no nearest-entry judgment calls were needed here.
- The overview page at `/v1/nodes/sec-supplier-due-diligence/body` describes four sub-pages (sanctions, code of conduct, disqualification, and "a fourth page covering the ongoing side") that turned out to be unrelated to answering this specific question — the real answer lives in the origin/value/goods row table, not in that onboarding-focused narrative. Worth noting so a future walk doesn't waste time chasing that fourth page for a periodic-review answer that's actually on the row itself.
