1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "MD, Singapore, one night — hotel cap per night, and receipt threshold above which receipt required" --member /v1/regions/expense "business trip lodging rates and receipt rules likely here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_cb64a6 --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 303 USD per night. Receipt required above: 39 USD (receipt threshold). This is the current overseas per-diem table, in force from 2026-01-01, which covers today's date (2026-09-21).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body (the figures: 303 USD lodging/night, 39 USD receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms this version, effective 2026-01-01 onward, is the one that applies to today's date)

4. **Notes**:
The three legend tables (grade, band, stay) are separate documents from the row itself and have to be read individually to translate "managing director / Singapore / one night" into the G4/B2/S1 row address — nothing shorter gets you there, and the address cannot be guessed or built by hand.
The one place I nearly went wrong: there are three versions of the overseas per-diem document (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), and the legend-revision page warns explicitly that reaching for the newest is wrong for any question dated before 2026-01-01. This question is undated in itself but the walk's stated "today" is 2026-09-20/2026-09-21, which falls inside the current table's effective range, so `sec-hard-perdiem` was the right pick — but I checked the revision note explicitly rather than assuming, since it's exactly the kind of thing this domain flags as a common mistake.
Note there's also a `/v1/nodes/corp-card` table (card caps) and `/v1/nodes/evidence` table (what must be attached for a spend) surfaced in the same working set — I did not need either since the per-diem row itself already states the receipt threshold directly, but they looked like plausible alternate paths to the same answer at first glance.
