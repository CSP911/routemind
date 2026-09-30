1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "MD, Singapore, 4 nights - hotel per night limit and receipt threshold" --member /v1/regions/expense "hotel spend limits and receipt requirements for business trips are covered under expense"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s2/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b92f6f --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s2/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 307 USD per night. Receipt required above 42 USD (the receipt threshold on the same row). This is under the current overseas per-diem table (in force 2026-01-01 onwards), for grade G4 (managing director), band B2 (Singapore), stay S2 (four nights).

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s2/body

4. **Notes**:
The per-diem table has three superseded/current versions (overseas-rates, hard-perdiem-v2, sec-hard-perdiem) covering different date ranges, and the legend-revision doc warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20/21) falls inside the current table's range, so this wasn't actually ambiguous, but it's the kind of question where grabbing the first "per-diem" hit without checking the revision note would give the wrong figures for a trip dated in 2025. Also, the three qualifiers (grade/band/stay) each needed their own legend lookup to convert "managing director" / "Singapore" / "four nights" into row codes (G4/B2/S2) — the row itself never restates the plain-language inputs, only the codes, so skipping the legends would make the row address impossible to pick with confidence. One procedural note: I closed the overlay with `--used` addresses that were never added as overlay members (only the top-level /v1/regions/expense was a member) — the tool accepted it but flagged them as "reached ... somewhere the overlay never named" rather than tracked narrowing; worth adding leaf nodes as members via `overlay add` before closing in future walks.
