1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body
```

2. **Answer**
Lodging cap: 251 USD per night. Receipts are required above 44 USD (the receipt threshold).
(For context, same row also gives meals at 85 USD/day and incidentals at 17 USD/day, current table in force from 2026-01-01.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions applies to today's date)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body (the answer: lodging and receipt threshold figures)

4. **Notes**
The expense table's warning about three per-diem versions (`hard-perdiem-legend-revision`) was the one place it would have been easy to go wrong — the newest-looking table (`sec-hard-perdiem`) happens to be correct here since today (2026-09-20) falls after 2026-01-01, but the legend explicitly calls out that grabbing the newest table without checking the date is wrong for anything dated in 2025 or earlier. I checked the date against the revision table before trusting the current one rather than assuming.

The three qualifiers (grade, band, stay) each have their own legend and had to be resolved separately before the exact row address could be built — "department head" isn't itself a grade code, "Singapore" isn't a band code, and "three weeks" isn't a stay code; each needed a lookup. "Three weeks" mapped cleanly onto stay S4 ("three weeks") with no rounding judgment needed, which was a relief since the legend's fallback instruction ("take the nearest entry above it") suggested ambiguity might be involved elsewhere.

No separate "evidence" table (`/v1/nodes/evidence`) needed to be consulted — the receipt threshold for this specific claim type is given directly on the per-diem row itself, and using the general evidence table instead could have produced a different, wrong threshold if one exists there for other expense types.
