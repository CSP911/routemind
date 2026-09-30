1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Da Nang supplier, KRW 60,000,000, office consumables: site visit required? review frequency?" --member /v1/regions/procurement "vendor onboarding / due diligence and review cadence likely lives under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_fa238b --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body

2. **Answer**
No, no site visit is required. The file is re-reviewed every 24 months. (Also: screening score required is 82, financial statements needed cover the last year.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (established that the 2026-01-01-onward table applies, given today's date of 2026-09-20)
/v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
/v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
/v1/nodes/hard-diligence-legend-goods/body (office consumables → goods K1)
/v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body (the answer: Site visit = no, Re-review interval = every 24 months)

4. **Notes**
The near-miss here is version drift: the procurement table lists three separate supplier-due-diligence documents (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no obvious warning at the table level that they're mutually exclusive by date. It would have been easy to grab the wrong one, since "current" wasn't stated except inside `sec-hard-diligence`'s own description ("in force from 2026-01-01"). The `hard-diligence-legend-revision` page was the thing that made the date check explicit and confirmed today's date (2026-09-20) falls in the current version's window, so I read that before touching the row data.

The three-qualifier lookup (origin/value/goods) matched the question's numbers exactly and cleanly — Da Nang, sixty million won, and "just office consumables" are all listed verbatim in their respective legends, so there was no need to round to a nearest bucket, which the legends explicitly allow for if the input isn't a listed value.

One oddity: the overlay close command reported all five addresses I used as "reached ... from somewhere the overlay never named" rather than as originally-listed members, because I never ran individual `overlay add` calls for each address as I drilled down — I went straight from the initial member (`/v1/regions/procurement`) to reading files directly. The outcome was correctly recorded as answered regardless, but a stricter walk would have added each address to the overlay as it was opened.
