1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W1, goods K4: site visit required? file review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, matches today's date 2026-09-21" --member /v1/nodes/hard-diligence-legend-revision/body "warns diligence table has three versions with different effective dates - need to confirm which version applies"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_37cc62 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body

2. **Answer**:
No, a site visit is not required. The file (re-review) interval is every 36 months.
(For reference, screening score required is 65 and financial statements are not required.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is current for today's date, 2026-09-21)
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body (the row with the actual figures)

4. **Notes**:
The procurement area table warned upfront that supplier due diligence has three superseded versions in force over different date ranges, so before trusting the current table (`sec-hard-diligence`) I deliberately checked the legend-revision page to confirm 2026-09-21 falls in the "2026-01-01 onwards" band rather than assuming the newest table is automatically right. That was the only place a wrong turn was plausible — the row itself, once the origin/value/goods triple was known, was a direct, unambiguous lookup with no other candidate rows or conflicting figures.
