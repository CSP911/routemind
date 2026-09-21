1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In January 2024, nightly lodging cap for a trip to a band B destination under the overseas per-diem in force on that date" --member /v1/regions/expense "business trip pay / lodging cap likely lives here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-20_7adf96 --address /v1/nodes/hard-perdiem-legend-revision/body --why "explains which per-diem version is in force for a given date; Jan 2024 predates 2024-07-01 cutover"
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py overlay add --id ov_2026-09-20_7adf96 --address /v1/nodes/overseas-rates/body --why "oldest per-diem version, in force until 2024-07-01 - covers Jan 2024"
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7adf96 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/overseas-rates/body

2. **Answer**: USD 180 per night (band B: China, South-East Asia, Eastern Europe).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established that the version in force for January 2024 is the oldest one, "Overseas allowance and exchange rate," effective until 2024-07-01)
- /v1/nodes/overseas-rates/body (the actual figures: band B lodging cap USD 180/night)

4. **Notes**: The expense table's members list only surfaced `hard-perdiem-v2` (in force 2024-07-01 to 2025-12-31) and `sec-hard-perdiem` (current, from 2026-01-01) as direct overlay members — neither covers January 2024. The legend-revision doc was the key: it warned explicitly that there are three versions and that reaching for the newest is wrong, and that the oldest version isn't even labeled as superseded on its own page. The oldest version's address (`/v1/nodes/overseas-rates/body`) wasn't in the overlay's initial member list at all — I had to walk down through `/v1/nodes/travel-expense` → `/v1/nodes/travel-overseas` to find it. If I hadn't read the legend-revision doc first, it would have been easy to grab `hard-perdiem-v2` and answer with its band B figure instead, which would be wrong for a January 2024 date.
