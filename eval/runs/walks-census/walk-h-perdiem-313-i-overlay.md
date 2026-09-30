1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "MD, Singapore, 3-week trip: nightly hotel cap and receipt threshold" --member /v1/regions/expense "expense table covers business trip caps and receipt rules"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body
./bench/rmcli.py overlay add --id ov_2026-09-21_346c74 --address /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body --why "the exact row: MD (G4), Singapore (B2), 3 weeks (S4) — has lodging cap and receipt threshold"
./bench/rmcli.py overlay add --id ov_2026-09-21_346c74 --address /v1/nodes/hard-perdiem-legend-grade/body --why "resolves managing director to grade G4"
./bench/rmcli.py overlay add --id ov_2026-09-21_346c74 --address /v1/nodes/hard-perdiem-legend-band/body --why "resolves Singapore to band B2"
./bench/rmcli.py overlay add --id ov_2026-09-21_346c74 --address /v1/nodes/hard-perdiem-legend-stay/body --why "resolves three weeks to stay S4"
./bench/rmcli.py overlay add --id ov_2026-09-21_346c74 --address /v1/nodes/hard-perdiem-legend-revision/body --why "confirms current table (2026-01-01 onwards) applies for a 2026-09-21 question"
./bench/rmcli.py overlay close --id ov_2026-09-21_346c74 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body

2. **Answer**: Lodging (hotel) cap: 315 USD per night. Receipt threshold: 48 USD — spend above that amount requires a receipt (this is the current table, in force from 2026-01-01; applies since today, 2026-09-21, is after that date).

3. **Source** (in order used):
- /v1/nodes/hard-perdiem-legend-grade/body
- /v1/nodes/hard-perdiem-legend-band/body
- /v1/nodes/hard-perdiem-legend-stay/body
- /v1/nodes/hard-perdiem-legend-revision/body
- /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body

4. **Notes**: The overseas per-diem row is indexed by three separate qualifiers (grade, country band, stay length) that each need a legend lookup before the actual row address can be built — "managing director" isn't usable directly, it has to become "G4" via the grade legend, "Singapore" becomes "B2" via the band legend, and "three weeks" becomes "S4" via the stay legend. It would be easy to guess a plausible-looking row address without checking all three legends and get the wrong one silently. The bigger trap is the per-diem legend-revision page: there are three separate document versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onwards) with different structures, and the page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest document never states it was superseded — so a careless read of the oldest doc could look complete and correct while being stale. Today's date (2026-09-21) puts this squarely in the current table, so no correction was needed here, but I checked the revision page deliberately rather than assuming "newest = current" was safe.
