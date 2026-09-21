1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon company, 60M won, licence: on-site visit required? review frequency for file?" --member /v1/regions/procurement "amount thresholds, due diligence, site visits likely covered under procurement vendor rules"
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_70b842 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body
```

2. **Answer**
No site visit is required. The file's re-review interval is every 24 months. (Also on this row, though not asked: screening score required is 37, and financial statements needed are for the last year.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body — confirmed which of the three due-diligence table versions is in force for today's date (2026-09-20 → the current table)
- /v1/nodes/hard-diligence-legend-origin/body — Daejeon → origin O1
- /v1/nodes/hard-diligence-legend-value/body — sixty million won → value W2
- /v1/nodes/hard-diligence-legend-goods/body — a licence → goods K4
- /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body — the row with the actual figures (site visit: no; re-review interval: every 24 months)

4. **Notes**
- The subject exists in three superseding versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page warns explicitly that the oldest version says nothing about being replaced, so reaching for it directly would look right and be wrong. Checking the revision legend before touching the actual table was necessary, not optional — today's date puts the answer in the current table (`sec-hard-diligence`), but a question dated in 2025 would need the superseded `hard-diligence-v2` instead.
- The table is indexed by three independently-coded qualifiers (origin, value, goods) with three separate legend pages, none of which repeat each other's mappings. It would be easy to guess a code from pattern-matching (e.g. assuming region order matters) rather than actually reading each legend; I read all three explicitly rather than assuming.
- "A licence" in the goods legend is a literal, exact phrase match to the question's wording, which made goods K4 unambiguous — but it's worth flagging that this legend's phrasing is quite specific and a slightly different description of a licence-related purchase might not map so cleanly.
- No ambiguity remained once the three codes were resolved: O1/W2/K4 pointed to exactly one row, and that row had both requested figures stated plainly.
