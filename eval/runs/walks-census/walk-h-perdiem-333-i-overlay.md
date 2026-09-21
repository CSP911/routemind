1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "MD in Dhaka, 3 weeks: nightly hotel cap and receipt threshold?" --member /v1/regions/expense "hotel per-night cap and receipt requirement for business travel live here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body
./bench/rmcli.py table /v1/nodes/evidence
./bench/rmcli.py overlay close --id ov_2026-09-21_9b125c --outcome answered --used /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body

2. **Answer**
Lodging (hotel) cap: 347 USD per night.
Receipt required above: 66 USD.
(This is the current overseas per-diem table, in force from 2026-01-01, row for grade G4 / band B4 / stay S4: managing director, Dhaka, three-weeks stay.)

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body (confirmed 2026-09-21 falls under the current table, not the superseded ones)
/v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
/v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
/v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
/v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body (the answering row: lodging 347 USD/night, receipt threshold 66 USD)

4. **Notes**
The overseas per-diem subject has three superseded/current versions indexed by different numbers of qualifiers (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the warning page is explicit that reaching for the newest is wrong for a date before 2026-01-01. Today's date (2026-09-21) does fall inside the current table's range, so `sec-hard-perdiem` was correct, but this is exactly the kind of thing that's easy to skip past — I made sure to open the revision-legend and check the date before trusting the row rather than assuming "current" always means "current table."

All three qualifiers (grade, band, stay) happened to have exact, unambiguous matches in their legends ("a managing director" → G4, "Dhaka" → B4, "three weeks" → S4), so no nearest-entry judgment call was needed here — this was more clear-cut than the legend instructions ("if not listed, take the nearest entry above it") implied might be necessary.

I briefly opened the general `/v1/nodes/evidence` table, thinking the "receipt threshold" figure on the per-diem row might only be a per-diem-specific number and that a separate, more general "above what amount must a receipt be kept" rule might live in Evidence/Qualifying-evidence instead. That table turned out to cover a different question (which document TYPE qualifies as evidence — tax invoice vs. invoice vs. card slip — and simplified-invoice ceilings), not a threshold amount, so I did not descend into it further and used the per-diem row's own explicit "Receipt threshold: 66 USD" field as the answer. Worth flagging in case that general evidence table also has a numeric threshold that could conflict — I did not read `/v1/nodes/qualified-evidence` to fully rule that out.
