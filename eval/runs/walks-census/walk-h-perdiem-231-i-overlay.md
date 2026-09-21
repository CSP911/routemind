1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dhaka, department head, 4 nights: hotel per-night cap and receipt threshold" --member /v1/regions/expense "hotel per-night amount and receipt requirement for a business trip should be here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e680e0 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body

2. **Answer**: Lodging cap is 275 USD per night. A receipt is required above 56 USD (the receipt threshold). (Not asked, but on the same row: meals 103 USD/day, incidentals 21 USD/day.) This is the current table, in force from 2026-01-01, and applies as of today (2026-09-20/21).

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body — department head → grade G3
/v1/nodes/hard-perdiem-legend-band/body — Dhaka → band B4
/v1/nodes/hard-perdiem-legend-stay/body — four nights → stay S2
/v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body — the figures (lodging 275, receipt threshold 56)

4. **Notes**:
- "Four nights" mapped exactly onto the legend's "four nights" → S2 — no rounding/nearest-entry judgment call needed there, unlike grade/band which are also exact matches here (department head → G3, Dhaka → B4). All three lookups were unambiguous, which is worth flagging precisely because the legends warn "if what you have is not listed, take the nearest entry" — I checked for that trap and it didn't apply this time.
- The table `/v1/nodes/sec-hard-perdiem` warns of THREE versions of this per-diem table with different effective dates (`hard-perdiem-legend-revision`, `hard-perdiem-v2` superseded, and the current one). I read the in-force dates printed directly on the row itself ("In force from 2026-01-01") rather than opening the separate revision-legend doc, since the row's date range alone was enough to confirm it's current versus today's date (2026-09-20/21). Worth being careful here: it would be easy to grab a superseded row (e.g. `hard-perdiem-v2`) if not checking the effective date.
- The overlay's own row list under `/v1/regions/expense` did not include the four addresses I actually used (the legends and the specific grade/band/stay row) — those only appeared after opening `/v1/nodes/sec-hard-perdiem` as a table, one hop further. The close command accepted them but flagged them as "reached = answered from somewhere the overlay never named" rather than a clean match against overlay members. This is a mechanical/procedural nuance, not a factual uncertainty — the answer itself is not in doubt.
