1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Team manager, Singapore, 3 weeks - hotel nightly cap and receipt threshold" --member /v1/regions/expense "business trip lodging allowance and receipt rules likely here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4b9fff --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body

2. **Answer**: $187 per night on lodging (the cap), and the receipt must be kept for anything above $40 (the receipt threshold). This is from the current overseas per-diem table (in force 2026-01-01 onward), for grade G2 (team manager), band B2 (Singapore), stay S4 (three weeks).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body

4. **Notes**: The near-miss here was the version warning — `hard-perdiem-legend-revision` flags that overseas per-diem has three superseded-but-undeclared versions (`overseas-rates` until 2024-07-01, `hard-perdiem-v2` 2024-07-01 to 2025-12-31, and `sec-hard-perdiem` from 2026-01-01), and the oldest one never says it was replaced. Today is 2026-09-21, so the current table applies, but had I skipped that legend I could easily have grabbed the wrong version by just landing on the first per-diem-looking node in the overlay listing. The three-way legend lookup (grade/band/stay) was mechanical once found, and "three weeks" mapped exactly to stay S4 with no rounding needed. One oddity: closing the overlay reported all five sources as "reached" rather than as named overlay members, because I only added the top-level `/v1/regions/expense` as a member and then drilled down freely via `table`/`read` rather than adding each node with `overlay add` — the tool still accepted them as used sources, but that's a gap between how the overlay is meant to be narrowed (via add/remove) and how I actually worked it.
