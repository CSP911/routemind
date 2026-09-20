1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body

2. **Answer**:
For grade G1, band B3, stay S4 (in force since 2026-01-01, current as of today 2026-09-20):
- Lodging: up to 139 USD per night
- Receipt required above: 45 USD (the receipt threshold)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body

4. **Notes**:
The expense area lists three versions of the overseas per-diem (current `sec-hard-perdiem` since 2026-01-01, superseded `hard-perdiem-v2` for 2024-07-01–2025-12-31, and an older `overseas-rates`). It would be easy to grab the wrong version if you didn't check `hard-perdiem-legend-revision` or notice the "in force from" date — I confirmed today's date (2026-09-20) falls under the current table before trusting the row. The row address for G1/B3/S4 was printed exactly by the `sec-hard-perdiem` table listing, so no address construction was needed — all four qualifiers (grade, band, stay, and the fact that it's the current table) matched directly with no ambiguity. The row also reports a separate "receipt threshold" (45 USD) distinct from the lodging cap (139 USD) and the meal/incidentals figures — worth being precise that the question's "keep the receipt" phrase maps to that specific field, not the lodging cap itself.
