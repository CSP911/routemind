1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body
```

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row: screening score required is 76; financial statements must be the last three years, audited.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established 2026-09-20 falls under the current, 2026-01-01-onward version)
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body (site visit: yes; re-review interval: every 6 months)

4. **Notes**
- Supplier due diligence has three superseded/current versions with overlapping subject matter (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the oldest version gives no indication it was ever replaced. It would have been easy to land on `/v1/nodes/supplier-due-diligence/body` first (it's listed right in the procurement area table with no obvious version warning) and stop there, since it looks complete on its own — it has no site-visit or re-review figures at all, which in hindsight was itself a clue it was the wrong version. Checking `hard-diligence-legend-revision` before trusting any one version was the thing that avoided a wrong answer.
- The current table is indexed by three separately-coded qualifiers (origin, value, goods) rather than by plain-language row names, so all three legend pages had to be resolved before the correct row address could even be constructed. None of the qualifiers were guessable from the question wording alone (e.g. "people's time" → goods K3 is not an obvious mapping).
- The overview page (`sec-supplier-due-diligence/body`) mentions "a fourth page covering the ongoing side of the same checks, re-run rather than one-off" but doesn't name it explicitly, which was a plausible distraction — it turned out not to be needed since the site-visit/re-review figures live directly on the origin/value/goods row, not on that fourth page.
