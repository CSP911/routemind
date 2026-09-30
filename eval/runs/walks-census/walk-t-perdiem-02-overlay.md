1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In September 2023, what was the nightly lodging cap for a trip to a band B destination? Answer under the version of the overseas per-diem that was in force on that date." --member /v1/regions/expense "expense area covers business trip pay including per-diem rates"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py overlay add --id ov_2026-09-20_bfe564 --address /v1/nodes/overseas-rates/body --why "oldest version, indexed by one qualifier, in force until 2024-07-01, covers Sept 2023"
./bench/rmcli.py overlay remove --id ov_2026-09-20_bfe564 --address /v1/nodes/hard-perdiem-v2/body --why "in force 2024-07-01 to 2025-12-31, not applicable to Sept 2023"
./bench/rmcli.py overlay remove --id ov_2026-09-20_bfe564 --address /v1/nodes/sec-hard-perdiem --why "current table from 2026-01-01, not applicable to Sept 2023"
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bfe564 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/overseas-rates/body

2. **Answer**: USD 180 per night, for band B (China, South-East Asia, Eastern Europe), under the oldest overseas per-diem version ("Overseas allowance and exchange rate"), which was in force until 2024-07-01 and so covers September 2023.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (establishes which of the three per-diem versions is in force for a given date)
- /v1/nodes/overseas-rates/body (the actual band table with the lodging cap figures)

4. **Notes**: The trap here is real — the expense area's table lists the current per-diem table (sec-hard-perdiem, in force from 2026-01-01) and a "v2" table (hard-perdiem-v2, 2024-07-01 to 2025-12-31) right at the top, both looking authoritative, while the oldest version that actually covers September 2023 isn't listed in the expense area's own table at all — it only shows up one level down, inside travel-expense → travel-overseas as /v1/nodes/overseas-rates/body. The legend document (hard-perdiem-legend-revision) explicitly warns that the oldest version "says nothing at all about having been replaced," so nothing in the old document itself would have flagged that it wasn't current — reading the legend first was what kept me from grabbing the v2 or current table by reflex. My two `overlay remove` calls on hard-perdiem-v2 and sec-hard-perdiem errored (404, not in overlay) because those addresses were only ever printed as contents of the /v1/regions/expense table member, not as overlay members themselves — harmless, but worth noting the overlay tool distinguishes "row shown because a member table prints it" from "row added as its own member."
