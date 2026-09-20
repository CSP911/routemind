1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py read /v1/nodes/travel-expense/body
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body
./bench/rmcli.py table /v1/nodes/evidence

2. **Answer**
For a department head (grade G3) on a one-night (stay S1) trip to Dhaka (band B4), under the current overseas per-diem table (in force from 2026-01-01):
- Lodging cap: 271 USD per night
- Receipt threshold: 53 USD

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which per-diem version applies for a 2026-09-20 question)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → B4)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → S1)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body (lodging cap and receipt threshold figures)

4. **Notes**
The overseas per-diem subject has three superseding versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision page explicitly warns that the oldest version never says it was replaced — reaching for it directly (e.g. via `travel-overseas` → `overseas-rates`) would have silently given stale 2024-and-earlier figures. Checking today's date (2026-09-20) against the revision table before picking a row was the step that mattered; skipping it was the easiest way to go wrong here.

The row itself bundles both parts of the question — nightly lodging cap and receipt threshold — in one document, which made it easy to conflate this per-diem-specific "Receipt threshold" with a general evidence-attachment rule. I did not open `/v1/nodes/qualified-evidence` to check whether a separate, generic receipt-threshold rule exists that might interact with this one; the per-diem row's own field answered the question as asked, so I stopped there rather than risk pulling in an unrelated general rule not scoped to this per-diem trip.

The grade/band/stay legends each state "if what you have is not listed, take the nearest entry above it" — none of that fallback was needed here since "department head," "Dhaka," and "one night" were exact matches in their respective legends, but it's worth flagging as a place where a slightly different wording of the question could have required a judgment call.
