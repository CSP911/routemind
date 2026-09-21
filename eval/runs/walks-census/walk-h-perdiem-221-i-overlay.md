1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Jakarta, 4 nights — hotel cap per night and receipt threshold" --member /v1/regions/expense "business trip / hotel spend and receipt rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4cfe86 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body

2. **Answer**:
Hotel (lodging) cap: 259 USD per night. Receipt required above: 47 USD (the receipt threshold). (For reference, the same row also gives meals at 89 USD/day and incidentals at 18 USD/day, but those weren't asked for.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions is in force for today's date, 2026-09-21)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body (the figures: lodging 259 USD/night, receipt threshold 47 USD)

4. **Notes**:
The overseas per-diem subject has three versions in force over different date ranges (until 2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that "the oldest says nothing at all about having been replaced" — so guessing from the newest table without checking the date would have been an easy, silent mistake here. Today's date (2026-09-21) falls under the current table (`sec-hard-perdiem`, in force from 2026-01-01), so that part was unambiguous once checked, but I made a point of reading the revision-warning page first rather than assuming.

The per-diem table itself isn't a single document — it's indexed by three separate qualifiers (grade, band, stay-length), each with its own legend translating plain-language input ("department head", "Jakarta", "four nights") into the row's actual codes (G3, B3, S2). None of these mappings are guessable — e.g. "team manager" is G2 but "department head" is G3, and Jakarta sits at B3, not obviously ordered by any factor I could have assumed (e.g., not simply cost-of-living rank as commonly perceived). Skipping any one legend and guessing the code would have silently produced a wrong row with no error.

The row also lists a "receipt threshold" without saying explicitly it's per-category — I read it as the general receipt requirement threshold for this trip's spend, which most directly answers "above what amount do I have to keep the receipt." No separate hotel-specific receipt rule was found elsewhere in the working set, and the row's own header covers lodging, meals, and incidentals together, so I'm treating it as trip-wide rather than hotel-only.
