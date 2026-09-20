1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/overseas-rates/body

2. **Answer**: USD 180 per night (Band B lodging cap under the oldest per-diem version, in force until 2024-07-01).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (identified which version applies to a January 2024 date)
- /v1/nodes/overseas-rates/body (the applicable version, with the Band B figures)

4. **Notes**: The expense table listed the current per-diem table (`sec-hard-perdiem`, since 2026-01-01) and the second version (`hard-perdiem-v2`, 2024-07-01 to 2025-12-31) directly, but not the oldest version — it was easy to assume one of those two was the answer. The legend-revision doc warned explicitly that reaching for the newest table is wrong for dates before 2026-01-01, and that a 2025 date needs the middle version specifically — but January 2024 predates even that middle version's start (2024-07-01), so neither listed table applies. The oldest version was addressed only by name (`overseas-rates`), not a full path, in the legend doc; it turned out to be nested under /v1/nodes/travel-overseas rather than a direct child of the expense area, so I had to walk down through travel-expense → travel-overseas to reach it. The legend doc's note that "the oldest says nothing at all about having been replaced" was the key warning — without it, opening overseas-rates/body alone would look like a valid, current answer with no clue it had been superseded.
