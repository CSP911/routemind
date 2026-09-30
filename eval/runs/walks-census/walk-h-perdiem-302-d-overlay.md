1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G4, band B1, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night limits and receipt threshold are expense policy topics"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3
./bench/rmcli.py overlay close --id ov_2026-09-21_482bac --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3

2. **Answer**
Lodging cap: 295 USD per night. Receipt threshold: 36 USD (above this amount a receipt must be kept). This is the row in force from 2026-01-01, current as of today (2026-09-21). For completeness, the same row also gives meals at 75 USD/day and incidentals at 15 USD/day, though those weren't asked for.

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3

4. **Notes**
- The opening `table` at /v1/regions/expense listed twenty candidate rows, several of which sounded plausible (`sec-trip-days-versus-allowance-days`, `travel-expense`, `evidence`). `sec-hard-perdiem`'s description ("THE CURRENT OVERSEAS PER-DIEM TABLE... by grade, band, stay") was the only one that named grade/band/stay explicitly, which is what made it the obvious pick over the others.
- Real risk of grabbing a stale version: the working set surfaced `hard-perdiem-legend-revision` (a warning that the table has three versions) and `hard-perdiem-v2` (marked SUPERSEDED, 2024-07-01 to 2025-12-31) alongside the current table. Had I opened `hard-perdiem-v2` instead of drilling into `sec-hard-perdiem`, I'd have pulled last year's numbers. The row I eventually read confirms it's the 2026-01-01 version and cross-references the older ones, so I'm confident this is current, but it would be easy to answer from the wrong vintage if you didn't notice the version warning up front.
- I never added `sec-hard-perdiem` or the final row as overlay members before reading them — I just followed `table`/`read` directly. The close command reported the used address as "reached" rather than a named overlay member, i.e. it flagged that I answered from an address the overlay never explicitly held. The answer is still correct, but the working-set discipline (add members with reasons as you narrow) wasn't fully followed here — worth doing explicit `overlay add` calls as you drill into sub-tables rather than just navigating past the overlay.
