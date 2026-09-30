1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G4, band B3, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "expense region covers business trip per diem/hotel caps and receipt thresholds"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ed1143 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body

2. **Answer**: Lodging (hotel) cap is 319 USD per night. Receipts must be kept for any spend above 48 USD (the receipt threshold). Both figures come from the per-diem table in force from 2026-01-01, which is current as of today (2026-09-21).

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body

4. **Notes**: The expense region table lists several near-miss candidates — `hard-perdiem-v2` (superseded, in force 2024-07-01 to 2025-12-31) and `hard-perdiem-legend-revision` (a warning node about there being three versions of this table). It would be easy to grab the wrong version's figures if you didn't check the "in force from" date against today's date (2026-09-21) — the row I used explicitly states it's the 2026-01-01 version, so it's current. I went straight to `sec-hard-perdiem` and drilled into the exact grade/band/stay row rather than reading the legend files, since the question already gave grade/band/stay codes directly (G4/B3/S1) rather than descriptions needing translation. Also: I closed the overlay citing the row address without first adding it as a member via `overlay add` — the tool flagged this as "reached" (answered from somewhere the overlay never named) rather than a clean match against a named member. Worth adding members explicitly before closing next time.
