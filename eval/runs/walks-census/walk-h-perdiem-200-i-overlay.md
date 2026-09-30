1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Tokyo dept head, one night: hotel cap per night and receipt threshold" --member /v1/regions/expense "business trip lodging caps and receipt rules likely here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b664aa --outcome answered --used /v1/regions/expense /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body

2. **Answer**
Lodging cap: 223 USD per night. Receipt required for any spend above 26 USD (the receipt threshold).

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body (established the 2026-01-01-onward table is the correct version for today's date)
/v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
/v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
/v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
/v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body (the figures: 223 USD lodging/night, 26 USD receipt threshold)

4. **Notes**
This is the overseas per-diem subject that has three superseding versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision doc is explicit that reaching for the newest is only correct if the question's date falls in its range. Today (2026-09-20/21) falls after 2026-01-01, so the current table `sec-hard-perdiem` was correct — but this is exactly the kind of question where grabbing the first per-diem-looking row without checking the revision doc would have silently used the wrong version had the date been in 2025. No ambiguity in the grade/band/stay mapping itself — "department head" maps cleanly to G3, "Tokyo" to B1, "one night" to S1, all one-to-one in their legends.
