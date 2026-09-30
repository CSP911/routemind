1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Dhaka, one night — hotel cap per night and receipt threshold?" --member /v1/regions/expense "business trip expense rules likely cover hotel per-night caps and receipt requirements by grade/city"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_98ea57 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: Lodging cap is 271 USD per night. Any spend above 53 USD requires a receipt (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body

4. **Notes**: The overseas per-diem table is indexed by three codes (grade, band, stay) that have to be looked up separately before the actual row address can even be constructed — "department head" → grade G3, "Dhaka" → band B4, "one night" → stay S1. It would be easy to skip the legends and guess at an address, but the tool warns never to build one, and the legend lookups are exactly what make the row address knowable in the first place. The other near-miss was the per-diem version: there are three versions of this table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) and the legend-revision doc explicitly warns that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-21) is safely inside the current version's range, but I checked the revision doc explicitly rather than assuming, since a question dated a year ago would need the superseded `hard-perdiem-v2` table instead. Also worth flagging: the overlay's own initial member list only had top-level section tables (e.g. `sec-hard-perdiem`), not the specific row/legend files — those were reached by drilling down through `table`/`read`, not via `overlay add`, and the close command reported them as "reached ... from somewhere the overlay never named," which is expected since the overlay is a coarse working set, not an exhaustive path.
