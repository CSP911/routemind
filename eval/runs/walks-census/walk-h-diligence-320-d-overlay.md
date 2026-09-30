1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W3, goods K1, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "diligence/site-visit requirements and review frequency by origin/value/goods tier sound like procurement vendor due diligence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_580e56 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body
```

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Full row for context: screening score required 86, financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is in force for today's date)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body (the answer)

4. **Notes**
- Supplier due diligence has three versions covering different date ranges, and the oldest one gives no indication it was ever superseded — checking the legend/revision page first was necessary to avoid silently reading the wrong era's rules. Today's date (2026-09-20) falls under the current table (`sec-hard-diligence`, in force from 2026-01-01), so that's the version used.
- The current table happens to already be indexed by exactly the three qualifiers in the question (origin, value, goods), so there was a single exact-match row (`hard-diligence-row-origin-o4-value-w3-goods-k1`) with no interpolation or nearest-match judgment needed.
- The row's body ends with a boilerplate-looking "If the figures are exceeded" section about excess costs/budget holder approval, which reads like it belongs to an expense/spend-limit template rather than a site-visit/re-review schedule. It doesn't answer anything asked here and I ignored it, but it's worth flagging as an odd carryover in the document.
