1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Team manager, Singapore, one night — hotel per-night cap and receipt threshold?" --member /v1/regions/expense "how much a business trip pays, per-diem/hotel caps and receipt rules"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c3c7bb --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body /v1/nodes/hard-perdiem-legend-revision/body
```

2. **Answer**
Lodging cap: **175 USD per night**. Receipt threshold: any spend **above 31 USD** requires a receipt (this is the "Receipt threshold" figure on the applicable row). This is for grade G2 (team manager), band B2 (Singapore), stay S1 (one night), under the per-diem table in force since 2026-01-01.

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body (the figures: 175 USD lodging, 31 USD receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms today's date, 2026-09-21, falls under the current table and not one of the two superseded versions)

4. **Notes**
- The overseas per-diem area has three superseded/current versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the table itself warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being replaced. It would have been easy to just grab `sec-hard-perdiem` without checking — I verified today's date (2026-09-21) actually falls in its 2026-01-01+ range before trusting it.
- The three legends (grade, band, stay) have to be resolved separately and combined into one row address (`hard-perdiem-row-grade-g2-band-b2-stay-s1`); nothing in the table itself states these mappings, so skipping any one legend would have made it impossible to construct the correct row address.
- The question asks two things (hotel cap and receipt threshold) that turned out to live in the same single row, which was not obvious until reading it — I initially expected to need a separate "evidence" node for the receipt-threshold question but the per-diem row already carried it.
- `overlay close` reported the used addresses as "reached" rather than as originally-named overlay members, since the drill-down went through `/v1/nodes/sec-hard-perdiem` rather than adding each leaf address to the overlay explicitly — this is just a bookkeeping note from the tool, not an error.
