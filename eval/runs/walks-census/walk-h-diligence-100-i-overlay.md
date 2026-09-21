1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 8,000,000, office consumables only: is a site visit required, and how often is the vendor file reviewed again?" --member /v1/regions/procurement "vendor/supplier due diligence, site visit requirement, and review cadence would be under procurement"
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a7060d --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body
```

2. **Answer**
No site visit is required. The vendor's file is re-reviewed every 36 months. (Also on this row, for context: screening score required is 46, and financial statements are not required.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body — maps "a firm in Stuttgart" to origin O2
- /v1/nodes/hard-diligence-legend-value/body — maps "eight million won" to value W1
- /v1/nodes/hard-diligence-legend-goods/body — maps "just office consumables" to goods K1
- /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body — the row with the actual figures (site visit: no; re-review interval: every 36 months)

4. **Notes**
- The procurement region table lists three diligence documents with scary "SUPERSEDED"/"THREE versions" warnings (`hard-diligence-v2`, `hard-diligence-legend-revision`, `sec-hard-diligence`). It would be easy to grab the wrong version. `sec-hard-diligence` is explicitly labeled as the current table, in force from 2026-01-01, which covers today's date (2026-09-20/21), so I used it and never opened the superseded `hard-diligence-v2` or the legend-revision page — didn't need to, since the current table's own "in force from 2026-01-01" note already answers the version question.
- All three lookups (origin, value, goods) were exact matches in their legends — no fuzzy "nearest entry above it" judgment calls were needed here, which is good because the legend text warns that such judgment calls should be recorded with the claim.
- Minor housekeeping oddity: the overlay was created with only `/v1/regions/procurement` as a declared member. The row-selection detour through `sec-hard-diligence` and the three legend files was done via plain `table`/`read` calls rather than `overlay add`, so the close command reported those addresses as "reached" (answered from somewhere the overlay never named) rather than as tracked members. Doesn't change the answer, but if the tracked working set is meant to be a complete trail, I should have `overlay add`-ed each legend/row address as I opened it instead of reading them ad hoc.
