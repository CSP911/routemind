1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body

2. Answer
Yes, a site visit is required. The file is re-reviewed every 6 months.
(For reference, this row also requires a screening score of at least 58 and audited financial statements for the last three years.)

3. Source
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body

4. Notes
Supplier due diligence exists in three versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), each covering a different date range, and the oldest version gives no indication that it was ever superseded. It would have been easy to land on the wrong version by following the plain "supplier-due-diligence" name or by grabbing the first search-like hit. I deliberately read `hard-diligence-legend-revision` first to confirm which of the three applies to today's date (2026-09-20) before touching any row data — that page explicitly warns the current table is only correct from 2026-01-01 onward, and for a 2025-dated question the correct answer would have come from `hard-diligence-v2` instead. The procurement table listing also carries an approval-threshold set of pages (`hard-threshold-*`) with the same three-version trap; easy to grab the wrong sibling table by pattern-matching the name instead of reading the "why" column. The current table (`sec-hard-diligence`) is indexed by exactly the three qualifiers named in the question (origin/value/goods), so once the correct version was confirmed, the target row address was constructable directly from the pattern the table's own listing showed for other rows — no ambiguity there.
