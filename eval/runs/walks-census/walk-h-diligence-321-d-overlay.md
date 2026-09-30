1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O4, value W3, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision "warns of three versions with different date ranges - need to confirm which applies today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_28a09d --outcome answered --used /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body /v1/nodes/hard-diligence-legend-revision/body
```

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Also on this row, for context: screening score required is 87, and financial statements for the last two years are required.)

3. **Source**
- `/v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body` (the site visit / re-review figures)
- `/v1/nodes/hard-diligence-legend-revision/body` (confirms this is the version in force for today's date, 2026-09-21)

4. **Notes**
- The procurement table lists three superseded/current pairs of pages for this subject (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) plus a legend-revision page warning about exactly this trap: reaching for the newest version is wrong for dates before 2026-01-01. Today (2026-09-21) is safely inside the current version's range (2026-01-01 onwards), so no ambiguity here, but this is the kind of question where checking the date explicitly mattered rather than assuming "current" is always right.
- The overlay I created only named the section header (`sec-hard-diligence`) and the legend-revision page as members; the tool auto-expanded the working set to all 64 individual origin/value/goods row addresses under that table. The exact row I read and cited was one of those auto-expanded rows, not one I'd explicitly added — closing the overlay flagged both used addresses as "reached" (answered from somewhere the overlay never named) rather than a clean match against explicit members. Worth being deliberate next time: add the specific row as a member once identified, rather than relying on the auto-expansion.
