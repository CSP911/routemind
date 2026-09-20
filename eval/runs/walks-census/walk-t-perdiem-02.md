1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/overseas-rates/body

2. **Answer**: USD 180 per night (Band B lodging cap under the original "Overseas allowance and exchange rate" version, in force until 2024-07-01 — the version covering September 2023).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established which version is in force for the date)
- /v1/nodes/overseas-rates/body (the actual figure)

4. **Notes**: The expense area table lists two per-diem tables directly (`hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and `sec-hard-perdiem` as "the current" table from 2026-01-01), and calls the current table's presence explicit while noting "the older band-only caps are still here and are superseded" — easy to misread as meaning only two versions exist, with the oldest just being a deprecated leftover of `hard-perdiem-v2`. The legend document at `hard-perdiem-legend-revision` clarifies there are actually three versions, and that the oldest ("Overseas allowance and exchange rate," at `overseas-rates`) covers anything before 2024-07-01 — which is what September 2023 needs. That oldest version's address was not printed anywhere in the `/v1/regions/expense` table itself; it only surfaces two levels deeper, under `travel-expense` → `travel-overseas`. The legend body names it as `overseas-rates` in a markdown table, but that is prose, not a printed address row — I did not use that string directly and instead located the real printed address (`/v1/nodes/overseas-rates/body`) via `travel-overseas`'s table listing. The legend also explicitly flags that "the oldest says nothing at all about having been replaced," so reading `overseas-rates/body` alone without checking the legend first would give no hint that a newer version exists or that this is the version to trust for a 2023 date — the versioning is only decidable from the legend, not from either per-diem document itself.
