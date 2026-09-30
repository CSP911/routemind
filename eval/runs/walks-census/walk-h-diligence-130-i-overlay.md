1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Stuttgart vendor, 700M KRW, office consumables: on-site visit required? re-review frequency?" --member /v1/regions/procurement "vendor due diligence, site visit and periodic review rules by category/amount/location live here"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2355de --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(For context: this row also requires a screening score of 58 and audited financial statements for the last three years.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body — confirmed which of the three due-diligence versions is in force today (2026-09-21 falls after 2026-01-01, so the current table applies, not the superseded ones)
/v1/nodes/hard-diligence-legend-origin/body — Stuttgart maps to origin O2
/v1/nodes/hard-diligence-legend-value/body — seven hundred million won maps to value W4
/v1/nodes/hard-diligence-legend-goods/body — just office consumables maps to goods K1
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body — the row itself, giving "Site visit: yes" and "Re-review interval: every 6 months"

4. **Notes**
- All three qualifiers in this question happened to be listed verbatim in their legends (Stuttgart, seven hundred million won, just office consumables), so there was no ambiguity about which codes to use or any need to fall back to "nearest entry above."
- The real trap here was the version, not the row. The current supplier due diligence table (`sec-hard-diligence`) only took effect 2026-01-01, and there's a dedicated legend-revision page warning that reaching for the newest table is wrong for anything dated before that. Today is 2026-09-21, so the current table is correct, but I deliberately checked the revision page before trusting the row rather than assuming "current" was safe — for a question dated in late 2025 the answer would have come from `hard-diligence-v2` instead.
- Mechanical note: I read the four legend files and the row file directly with `read` rather than adding them to the overlay one-by-one with `overlay add`. The `overlay close --used` call still accepted them and logged them as "reached = answered from somewhere the overlay never named," so nothing was lost, but the overlay's row listing itself never shows these as formal members — worth being deliberate about `add`ing next time if the working set is meant to reflect the actual path taken.
