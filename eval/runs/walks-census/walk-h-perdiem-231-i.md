1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body

2. Answer

Lodging cap: 275 USD per night.
Receipt threshold: above 56 USD, a receipt must be kept.

(Department head = grade G3, Dhaka = band B4, four nights = stay S2, under the per-diem table in force from 2026-01-01, which covers today's date 2026-09-20.)

3. Source

/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body

4. Notes

The expense area's table listing flagged upfront that overseas per-diem has three superseded versions living side by side under different addresses (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and that the oldest one says nothing about being replaced — so naively picking the first per-diem-looking table would have been silently wrong for a stale date. Checked the revision-legend file first and confirmed today (2026-09-20) falls under the current table (2026-01-01 onward), so no version confusion here, but it's the kind of thing that's easy to get wrong by reflex.

"Four nights" mapped exactly onto stay code S2 with no rounding needed — the legend bands "one/four/eight nights/three weeks" into S1–S4, and four nights is a listed value, not an interpolation, so there was no judgment call there either. Same for Dhaka → B4 and department head → G3: both direct hits in their legends, nothing nearest-neighbor about it.

One thing worth flagging: the row's "Receipt threshold" field isn't explicitly labeled as being about hotel/lodging specifically — it's one figure per row, sitting alongside lodging, meals, and incidentals, and it isn't tied to any one of those three by name. I read it as the general per-spend receipt threshold for this trip profile rather than something hotel-specific, since nothing in the row or its legends splits it out further. Didn't check the general `evidence` table in the expense area, since this row already gave a number directly responsive to the question and pulling in a second, possibly differently-scoped threshold seemed more likely to confuse the answer than sharpen it.
