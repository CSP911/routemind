1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In March 2023, what was the nightly lodging cap for a trip to a band B destination, under the overseas per-diem policy in force then?" --member /v1/regions/expense "expense table covers business trip pay including per-diem rates"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-20_eb8570 --address /v1/nodes/overseas-rates --why "legend says pre-2024-07-01 dates are answered by the original overseas-rates doc"
./bench/rmcli.py table /v1/nodes/overseas-rates
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py overlay add --id ov_2026-09-20_eb8570 --address /v1/nodes/overseas-rates/body --why "the actual document with the region band table; found band B lodging cap = USD 180"
./bench/rmcli.py overlay close --id ov_2026-09-20_eb8570 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/overseas-rates/body

2. **Answer**: USD 180 per night (band B: China, South-East Asia, Eastern Europe). The daily allowance for the same band is USD 80.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established that March 2023 falls under the "until 2024-07-01" version)
- /v1/nodes/overseas-rates/body (the actual rate table: Band B lodging = USD 180)

4. **Notes**: This is the exact trap the legend page warns about — overseas per-diem has three versions in force over different date ranges (original `overseas-rates` until 2024-07-01, `hard-perdiem-v2` from 2024-07-01 to 2025-12-31, and `sec-hard-perdiem` as the current table from 2026-01-01). The initial overlay's working set surfaced `sec-hard-perdiem` (labeled "THE CURRENT ... TABLE") and `hard-perdiem-v2` prominently, but neither covers March 2023 — reaching for either would have been wrong. It also explicitly warns that "the oldest [version] says nothing at all about having been replaced," so nothing in the `overseas-rates` document itself would have flagged that it was superseded; without first reading the legend page, I'd have had no reason to doubt it. The `overseas-rates` node itself wasn't in the original overlay member list and had to be added by hand after reading the legend. One overlay `add` on `/v1/nodes/overseas-rates` (without `/body`) returned "(nothing here)" — the file address needed the `/body` suffix, matching the pattern seen on the other file-type rows.
