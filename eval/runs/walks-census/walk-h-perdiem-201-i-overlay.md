1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Tokyo, four nights - hotel per-night limit and receipt threshold?" --member /v1/regions/expense "trip/hotel allowance and receipt rules live under expense"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_0fb77e --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body

2. **Answer**:
Lodging cap: 227 USD per night. Receipt threshold: 29 USD — spend above that amount requires a receipt to be kept/attached (the row's other figures, for context: meals 61 USD/day, incidentals 12 USD/day). This is the current overseas per-diem table, in force from 2026-01-01, which covers today (2026-09-21).

3. **Source** (in order used):
- /v1/nodes/sec-hard-perdiem (table — the current overseas per-diem table, confirmed in force from 2026-01-01)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body (the figures: 227 USD lodging/night, 29 USD receipt threshold)

4. **Notes**:
The expense area's overlay listed two other per-diem documents alongside the current table — `hard-perdiem-legend-revision/body` (a warning that overseas per-diem has three versions with different dates) and `hard-perdiem-v2/body` (explicitly marked SUPERSEDED, in force 2024-07-01 to 2025-12-31). It would have been easy to grab the wrong version here; I didn't read the legend-revision doc directly, but the current table's own description states plainly "in force from 2026-01-01," which is before today's date (2026-09-21), so I trusted that instead of chasing the revision-history doc as a fourth hop.

The three-legend indirection (grade / band / stay each map plain-English inputs to a row code) is easy to get subtly wrong if you guess at the code instead of reading each legend — e.g. it would be natural to assume "department head" is the most senior grade (G4), but G4 is reserved for "managing director"; department head is G3. I read all three legends explicitly rather than guessing.

One bookkeeping note: `overlay close` reported the four addresses I used as "reached" rather than as overlay members, because I never called `overlay add` for them after drilling in from the expense table — I only registered `/v1/regions/expense` as a member at creation and then navigated by table/read directly. The tool still accepted and recorded them, but a stricter walk would have added each address to the overlay as I picked it.
