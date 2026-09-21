1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O2, value W1, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, likely holds the O2/W1/K2 row" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table, need to confirm which is in force today 2026-09-21" --member /v1/nodes/hard-diligence-v2/body "superseded 2024-07-01 to 2025-12-31 version, kept in case dates matter"
./bench/rmcli.py overlay remove --id ov_2026-09-20_75d961 --address /v1/nodes/hard-diligence-v2/body --why "confirmed by legend-revision: today 2026-09-21 falls under current table sec-hard-diligence, not the 2024-07-01/2025-12-31 version"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_75d961 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k2/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months.
(For reference, the full row also gives: screening score required 47, financial statements not required — under the current table, in force since 2026-01-01.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body — confirmed which of the three due-diligence table versions applies to today's date (2026-09-21 → current table, `sec-hard-diligence`)
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k2/body — the actual O2/W1/K2 row, source of the site-visit and re-review figures

4. **Notes**
- The question gives no date, so I used today (2026-09-21). This mattered: the procurement table listing flagged that supplier due diligence has three superseded/current versions, and the legend-revision page is explicit that reaching for the newest is wrong for anything dated before 2026-01-01. Since there's no date here, today applies and the current table (`sec-hard-diligence`, in force from 2026-01-01) is correct — but I only knew that for certain after reading the revision legend, not by assuming "current" means "right."
- Opening `/v1/nodes/sec-hard-diligence` as a table member auto-expanded into all 64 origin×value×goods row files plus the three legend files (goods/origin/value), which was a lot of noise in the working set, but it did print the exact leaf address for O2/W1/K2 directly, so no separate `table` lookup on that address was needed.
- The close command reported the row address as "reached from somewhere the overlay never named," even though it appeared in the initial overlay listing (as an expansion under the `sec-hard-diligence` member, not as a member I added myself). Worth flagging: naming the top-level table as a member doesn't register its expanded rows as tracked members, only whatever address you explicitly add/use.
- The row's "If the figures are exceeded" section reads like boilerplate about expense limits/excess claims — it doesn't fit a due-diligence page (screening score, site visit, re-review interval) and looks like a copy-paste artifact from an expense-type template. It's not part of the answer to this question and I ignored it, but it's the kind of thing that could mislead a reader skimming the row.
