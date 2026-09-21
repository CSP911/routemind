1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B1, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel nightly cap and receipt threshold are business trip expense policy"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4c0755 --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body

2. **Answer**: Lodging cap is 223 USD per night. The receipt threshold is 26 USD — spend above that amount requires a receipt.

3. **Source**:
/v1/nodes/sec-hard-perdiem/body (table pointing to the per-diem rows)
/v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body (the G3/B1/S1 row with the figures)

4. **Notes**: The expense area's overlay surfaced a warning up front — `/v1/nodes/hard-perdiem-legend-revision/body` flags that overseas per-diem has three versions (`hard-perdiem-v2` for 2024-07-01–2025-12-31, `overseas-rates` before that, and the current `sec-hard-perdiem` table from 2026-01-01). It would have been easy to grab a superseded rate table by name alone; the current table's own row explicitly states "In force from 2026-01-01," and today (2026-09-21) falls inside that, so I stayed on `sec-hard-perdiem` rather than second-guessing into the older versions. The G3/B1/S1 row was a direct, unambiguous match once the table was open — no legend lookups for grade/band/stay were needed since the question already gave the codes. One minor oddity: the overlay close reported the used addresses as "reached... from somewhere the overlay never named" since I never formally added the row-level address as a member before closing — worth noting but didn't affect the answer.
