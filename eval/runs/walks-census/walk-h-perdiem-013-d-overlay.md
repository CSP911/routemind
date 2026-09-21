1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B2, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip / hotel / per diem / receipt threshold rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b1dea3 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s4/body

2. **Answer**: Lodging cap is 123 USD per night. The receipt threshold is 36 USD — spend above that amount requires a kept receipt.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body
- /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s4/body

4. **Notes**: The overseas per-diem subject has three superseded/current versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision page warns that the oldest version says nothing about being replaced, so grabbing the first hit without checking dates would silently give a stale figure. Today's date (2026-09-21) falls after 2026-01-01, so the current table `sec-hard-perdiem` is the right one — this is the case the walk exists to get right, not the 2025-dated trap case. The row for grade G1 / band B2 / stay S4 existed as an exact, directly-indexed match, so no interpolation or legend lookups (grade/band/stay definitions) were needed. The overlay close reported the two addresses used as "reached" rather than "used from the named member list" since they were sub-rows navigated to under the `/v1/regions/expense` member rather than added as members themselves — cosmetic, didn't affect the answer.
