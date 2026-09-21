1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "MD, Dhaka, 4 nights: hotel per-night cap and receipt threshold" --member /v1/regions/expense "trip allowance and receipt rules for hotel spend live here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f86c64 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body

2. **Answer**
Lodging cap: 339 USD per night. Receipt required above 60 USD (the receipt threshold on this row).
(For context, this same row also gives meals at 112 USD/day and incidentals at 23 USD/day, though those weren't asked for.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed the current, 2026-01-01-onward table applies for a 2026-09-20 date)
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body (the figures themselves)

4. **Notes**
Overseas per-diem is versioned three ways (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) with overlapping, non-obvious date ranges, and the oldest version doesn't say it's been superseded — reading the legend-revision page first, before touching any figures, was the only way to be sure the 2026-01-01-onward table was the right one to use rather than defaulting to "newest" out of habit. The current table itself has no single "hotel + receipt" row — it's indexed by three separate legends (grade, band, stay) that each require a lookup before the actual figures can be found, so the real work was three small translations (managing director→G4, Dhaka→B4, four nights→S2) rather than a single lookup. Nothing here was ambiguous once the legend-revision warning was heeded; the main risk was grabbing `hard-perdiem-v2` or the current table without checking the date qualifier first.
