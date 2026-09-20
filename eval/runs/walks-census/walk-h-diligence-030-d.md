1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirms the current 2026-01-01 table applies to today's date)
/v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k1/body (the answer)

4. **Notes**
The procurement area warns up front that supplier due diligence has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and that "reaching for the newest is wrong for anything before 2026-01-01." Today is 2026-09-20, so the current table (`sec-hard-diligence`) is correct, but this was the one place it would have been easy to grab the wrong version without checking the date first. The question already gave the row's codes (O1, W4, K1) directly, so the origin/value/goods legend files were not needed — the row address was guessable straight from the table listing and matched exactly. No ambiguity beyond the version check.
