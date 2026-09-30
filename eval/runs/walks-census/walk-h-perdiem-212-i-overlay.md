1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Singapore, 8 nights: hotel per-night cap and receipt threshold?" --member /v1/regions/expense "trip allowances, per diem/hotel caps, and receipt requirements live in expense"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_21a005 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body

2. **Answer**:
Hotel lodging cap: 247 USD per night. Receipt threshold: 41 USD (spend above this amount requires a kept receipt).
(Department head = grade G3, Singapore = band B2, eight nights = stay S3, under the per-diem table in force from 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirms which of the three per-diem table versions applies to today's date, 2026-09-21 — the current one)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → B2)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → S3)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body (the figures: lodging 247 USD/night, receipt threshold 41 USD)

4. **Notes**:
The overseas per-diem area has three superseded/current table versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) covering different date ranges, and the legend-revision doc is explicit that reaching for the newest is wrong for a question dated before 2026-01-01 — worth checking every time even though today's date made the current table the obvious pick here. It would be easy to skip that check on a "current-looking" question and get lucky, then get burned on an older-dated one.
The three qualifiers (grade/band/stay) each need a separate legend lookup before the row address can be built — none of the wording in the question ("department head", "Singapore", "eight nights") appears directly in the row table, only in the legends. Rows are addressed by legend-translated codes, so skipping a legend and guessing the code would silently pick the wrong row rather than error.
The row's figures are denominated in USD, not the local currency (SGD) — the question's "Singapore" only selects the country band, not the payout currency; worth flagging since a reader might assume local currency.
Closing the overlay noted "reached = answered from somewhere the overlay never named" for all five sources used, since only the parent table `/v1/regions/expense` had been added as a formal overlay member — the legend and row documents were read directly via `table`/`read` navigation rather than added with `overlay add`. Not an error, just a reminder that overlay membership and actual navigation path can diverge.
