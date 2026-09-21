1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Nightly lodging cap for band B destination, version in force on 29 June 2024" --member /v1/regions/expense "per diem/lodging cap by destination band would be in expense policy"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py overlay add --id ov_2026-09-20_03fee0 --address /v1/nodes/overseas-rates/body --why "the pre-2024-07-01 version, in force on 29 June 2024, per the legend-revision note"
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py overlay close --id ov_2026-09-20_03fee0 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/overseas-rates/body

2. **Answer**: USD 180 nightly lodging cap for band B (China, South-East Asia, Eastern Europe).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/overseas-rates/body

4. **Notes**: The "first change" mentioned in the question is the 2024-07-01 switch from the oldest per-diem version (`overseas-rates`) to the second version (`hard-perdiem-v2`), which the legend-revision doc calls out explicitly — 29 June 2024 is two days before that cutover, so it falls under the oldest version, not the middle one. The near-miss here was going straight to `sec-hard-perdiem`, the table the expense region table currently advertises as "the overseas per-diem by grade, destination band and length of stay" — that's the 2026-01-01 current version and would have been the wrong answer entirely. The legend-revision doc's explicit warning ("reaching for the newest is wrong for anything before 2026-01-01," and "the oldest says nothing at all about having been replaced") is what caught this. The oldest version (`overseas-rates`) isn't listed as a member of `/v1/regions/expense`'s own table directly — it took two more hops through `travel-expense` → `travel-overseas` to find it, since the region table only surfaces the two newer versions by name.
