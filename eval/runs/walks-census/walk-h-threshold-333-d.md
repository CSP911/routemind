1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body

2. **Answer**: For category C4, amount V4, term M4 (delegation limit 100,063 thousand KRW): sign-off is by the CFO. Yes, prices must be obtained first — three competing quotes plus a written comparison are required before approval.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version is current for today's date, 2026-09-20)
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body (the answer)

4. **Notes**: The procurement table listing flagged that approval-threshold has three versions (a legend-revision warning), so I checked that page before trusting the "current" table — for a 2026 date the current table (`sec-hard-threshold`, in force from 2026-01-01) is correct, but this was a real branch point since a 2025-dated question would need `hard-threshold-v2` instead. No ambiguity on the row itself: the current table lists all 64 category/amount/term combinations directly, and C4/V4/M4 was a direct hit with no lookup of separate legends needed since the question already gave the coded values (C4, V4, M4) rather than plain-language descriptions.
