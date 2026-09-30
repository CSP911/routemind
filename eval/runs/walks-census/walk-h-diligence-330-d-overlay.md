1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O4, value W4, goods K1, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, likely holds the O4/W4/K1 row" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three diligence versions, need to confirm which is current for today's date"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_044b2b --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months. (Also on this row: screening score required is 90, and audited financial statements for the last three years are required — included for context, not asked for.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three diligence table versions is current for today's date, 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body (the row itself, in force from 2026-01-01, holding the site-visit and re-review answers)

4. **Notes**
Supplier due diligence has three superseded/current versions indexed differently (one qualifier, two qualifiers, three qualifiers), and the revision-legend page is explicit that reaching for the newest is wrong for any question dated before 2026-01-01, and that the oldest version says nothing about being replaced — a trap if you land on it first without checking dates. Today's date (2026-09-20) falls cleanly in the "2026-01-01 onwards" current-table window, so this wasn't ambiguous here, but it would have been easy to skip the legend check entirely since the overlay's initial member (/v1/nodes/sec-hard-diligence) already looked like "the current one" by name. I read the legend anyway to confirm rather than trust the label, which is the right habit given the page exists specifically to catch that mistake. The row address itself was guessable-looking (hard-diligence-row-origin-o4-value-w4-goods-k1) but I obtained it verbatim from the overlay listing rather than constructing it.
