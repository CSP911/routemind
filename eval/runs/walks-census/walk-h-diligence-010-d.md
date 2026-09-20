1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body

2. Answer: No site visit is required. The file is re-reviewed every 24 months. (For reference, this row's other figures: screening score required 34, financial statements from last year.)

3. Source:
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body — the row with the site-visit and re-review-interval figures
/v1/nodes/hard-diligence-legend-revision/body — confirmed the current (2026-01-01 onward) version applies for today's date, 2026-09-20
/v1/nodes/sec-hard-diligence/body — confirmed each row states checks, documents, and re-review interval together, and that rows are indexed by the three qualifiers given in the question

4. Notes: The procurement area warns upfront that supplier due diligence has three versions of the table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and that the oldest version says nothing about being superseded — so it would look valid even though it isn't for today's date. Checked the legend-revision page before touching any row to confirm the current table (`sec-hard-diligence`) was the right one for 2026-09-20, rather than assuming "current" was correct. The question already supplied the origin/value/goods codes (O1/W2/K1) directly, so the three legend pages (goods/origin/value) under `sec-hard-diligence` weren't needed — they exist to translate a person's plain-language description (job title, city, contract length) into these codes, which wasn't necessary here. No ambiguity in the final row: it states site visit and re-review interval side by side, unambiguously.
