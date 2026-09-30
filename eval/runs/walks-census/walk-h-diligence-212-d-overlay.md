1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O3, value W2, goods K3: is a premises visit required, and how often is the file reviewed again?" --member /v1/regions/procurement "vendor/goods classification with origin, value, goods codes and site-visit/review-frequency rules sound like procurement due diligence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_4bdb3d --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body

2. **Answer**: No, a site visit is not required. The file is re-reviewed every 24 months. (Also on the row: screening score required 68, financial statements from the last year — given for completeness, not asked.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established which of three versions applies for today's date, 2026-09-20)
- /v1/nodes/sec-hard-diligence (the current, in-force table — confirmed the O3/W2/K3 row exists here)
- /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body (the answer: Site visit = no, Re-review interval = every 24 months)

4. **Notes**: The domain has three superseded versions of the supplier due diligence table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page explicitly warns that the oldest version says nothing about being replaced — so jumping straight to a plausibly-named table without checking dates would have been an easy, silent mistake. Today's date (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` was the correct pick, but I checked the revision legend before reading any row to be sure rather than assuming "current" was right. The three question qualifiers (O3, W2, K3) mapped directly and unambiguously to one row address, so no interpretation was needed there. The overlay's close output labeled all three sources as "reached ... from somewhere the overlay never named" since I only registered the parent procurement table as a formal member — a quirk of the tool's bookkeeping, not a sign anything was wrong with the answer.
