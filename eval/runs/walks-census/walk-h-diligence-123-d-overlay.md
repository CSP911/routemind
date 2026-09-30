1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O2, value W3, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "diligence tiers, site visits, and file review cadence sound like vendor/procurement risk classification"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-20_ae38f2 --address /v1/nodes/sec-hard-diligence --why "current due diligence table (2026-01-01 onwards), indexed by three qualifiers: origin, value, goods"
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_ae38f2 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body
```

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(For reference, the full row also lists: screening score required 57, financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions is in force for today's date, 2026-09-20)
- /v1/nodes/sec-hard-diligence (the current table, opened to find the specific origin/value/goods row)
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body (the row with the actual answer)

4. **Notes**
- Supplier due diligence has three versions on file (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page is explicit that reaching for the newest one is wrong for any question dated before 2026-01-01. Today's date (2026-09-20) falls in the current version's range, so `sec-hard-diligence` was correct, but this was the one place I could easily have gotten it wrong by skipping the version check.
- The procurement table's first listing (under `/v1/regions/procurement`) surfaced a lot of near-miss rows — `sec-hard-threshold` (approval thresholds, not diligence), `sec-vendor-performance-and-renewal` (post-contract performance, not onboarding diligence), `vendor` (registration paperwork) — that share vocabulary with the question but answer a different one. Worth being deliberate about which of "due diligence" vs "approval threshold" vs "vendor registration" the question is actually asking.
- I initially tried to prune those near-miss rows out of the overlay with `overlay remove`, but they were never actual overlay members — they were just the contents of the `/v1/regions/procurement` table shown for context after adding that table as a member. The tool returned HTTP 404 "not in this overlay" for each, which clarified that only explicitly added members are removable; the printed table rows underneath a member are reference material, not part of the working set itself.
- The matched row's "If the figures are exceeded" section talks about an "excess" being settled or claimed with a budget-holder decision — boilerplate that reads like it was carried over from an expense/reimbursement policy and doesn't actually pertain to site visits or re-review cadence. Ignored it as irrelevant to this question.
