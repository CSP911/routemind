1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G4, band B1, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip hotel per diem and receipt threshold are expense topics"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e7774f --outcome answered --used /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging (hotel), per night: 287 USD. Receipt required above 30 USD (the receipt threshold). For reference, this row also lists meals at 65 USD/day and incidentals at 13 USD/day, though those weren't asked for.

3. **Source**:
- /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body (the figures)
- /v1/nodes/sec-hard-perdiem (table confirming this is the current, three-qualifier per-diem table in force from 2026-01-01)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms the 2026-01-01-onward version applies to a question dated 2026-09-21, not the superseded v2 or oldest overseas-rates version)

4. **Notes**:
This subject has three superseded versions of the same overseas per-diem table (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), each covering a different date range, and the oldest one gives no indication it was ever replaced. It would have been easy to grab the first per-diem-looking node without checking the revision legend and land on stale figures. Today's date (2026-09-21) falls after the 2026-01-01 cutover, so `sec-hard-perdiem` is correct, but I verified this explicitly against hard-perdiem-legend-revision rather than assuming "current" meant current. The row itself gave the exact G4/B1/S1 match directly with no ambiguity once the right table was open.
