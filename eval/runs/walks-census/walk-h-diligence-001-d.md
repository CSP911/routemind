1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body

2. Answer
No site visit is required. The file is re-reviewed every 36 months. (Screening score required: 31; financial statements not required.)

3. Source
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body

4. Notes
The procurement table listed both a current table (`sec-hard-diligence`, in force since 2026-01-01) and two superseded versions (`hard-diligence-v2` for 2024-07-01–2025-12-31, plus a legend-revision warning page implying a third, older version). It would have been easy to grab the wrong version's row by accident since the naming (`hard-diligence-v2`, `hard-diligence-legend-revision`) sits right next to the current set in the same table listing. I avoided that by going straight into `sec-hard-diligence` (explicitly labeled "THE CURRENT SUPPLIER DUE DILIGENCE TABLE") and confirmed via the row document itself, which states "In force from 2026-01-01" — matching today's date (2026-09-20) — and lists the two prior versions for reference rather than pointing to them as current. Didn't need to open the legend-revision page since the row's own validity note was unambiguous. The O1/W1/K2 combination had its own dedicated row (no interpolation across separate origin/value/goods legends needed), which made this a one-shot lookup once the right table was found.
