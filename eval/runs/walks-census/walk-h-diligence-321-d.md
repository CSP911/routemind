1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body
```

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Full row for reference: screening score required 87; financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirms which of the three due-diligence table versions is in force for today's date, 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body (the answer)

4. **Notes**
- The procurement area lists both an "approval threshold" subject and a "supplier due diligence" subject, each with three superseded versions and a legend-revision warning page. It would be easy to grab the wrong era's table — the legend-revision page explicitly warns that the oldest version says nothing about being replaced. Checked it before trusting `sec-hard-diligence` as current for 2026-09-20 (in force 2026-01-01 onwards).
- I initially opened `/v1/nodes/sec-supplier-due-diligence` (the "where to start" overview of four conceptual due-diligence pages — disqualification triggers, sanctions/ownership checks, code of conduct, etc.). None of those hold the O4/W3/K2 row data; the actual origin/value/goods matrix lives one level over, under `/v1/nodes/sec-hard-diligence`. Worth noting these two similarly-named tables (`sec-supplier-due-diligence` vs `sec-hard-diligence`) are easy to conflate.
- The row document ends with an "If the figures are exceeded" section about unapproved/unavoidable excess and budget-holder decisions — this reads like boilerplate carried over from an expense/threshold template and doesn't pertain to site visits or re-review cadence. Ignored it as not relevant to the question asked.
- Did not need the origin/value/goods legend files since the question already gave codes (O4, W3, K2) directly rather than descriptions needing translation.
