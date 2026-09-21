1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B4, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip pays / hotel per-night limit and receipt threshold likely here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e292cf --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body

2. **Answer**:
Lodging, per night: 283 USD. Receipt threshold: 62 USD (above this amount, evidence/receipt must be kept). This is from the current overseas per-diem table, in force from 2026-01-01 (today is 2026-09-21, so this version applies).

3. **Source**:
- /v1/nodes/sec-hard-perdiem/body (the current overseas per-diem table, confirmed 2026-01-01 is in force)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body (the row with the actual figures: 283 USD lodging/night, 62 USD receipt threshold)

4. **Notes**:
The overlay's member list only named the parent table (`sec-hard-perdiem`) and various sibling sections of expense; the exact row address (`hard-perdiem-row-grade-g3-band-b4-stay-s4`) only appeared once I opened `sec-hard-perdiem` as a table — it wasn't something I could have guessed or constructed. The overlay tool flagged this as "reached" rather than a listed member when closing, since I navigated straight to the row and its parent without adding them individually as overlay members first — worth noting in case that distinction matters for scoring.

The one place I could have gone wrong: `sec-hard-perdiem`'s description explicitly warns that overseas per-diem has three versions (current from 2026-01-01, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and an older `overseas-rates`). Today's date (2026-09-21) falls under the current table, so no version confusion applied here, but a walk on a different "as of" date would need to pick a different table entirely — this is an easy place to grab the wrong figures if the date isn't checked against the row's "in force" note.

The question says "hotel" and the table's field is literally "Lodging, per night" — same thing, just worth flagging the wording gap since a literal-match search on "hotel" would miss this row.
