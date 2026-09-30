1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G4, band B4, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01, likely holds hotel nightly cap for G4/B4/S1" --member /v1/nodes/hard-perdiem-legend-revision/body "warns which per-diem version covers which dates, need to confirm 2026-01-01 version is the right one for today 2026-09-21" --member /v1/nodes/evidence "evidence table may state receipt threshold above which a receipt must be kept"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_34e0b3 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s1/body

2. **Answer**:
Lodging cap: 335 USD per night. Receipt threshold: 57 USD (above this amount a receipt must be kept).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s1/body

4. **Notes**:
Overseas per-diem has three superseded/non-superseded versions covering different date ranges (until 2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend page is explicit that reaching for the newest is wrong for a question dated before 2026-01-01. Today is 2026-09-21, so the current table (`sec-hard-perdiem`, three qualifiers: grade/band/stay) is correct — but this was worth checking rather than assuming, since the region table listed both the current and the two older versions side by side. The per-row page for G4/B4/S1 directly answers both halves of the question (lodging cap and receipt threshold) in one table, so no separate trip to the general `evidence`/`qualified-evidence` tables was needed — the overlay member I picked for that (`/v1/nodes/evidence`) turned out to be unused, and the actual row I read wasn't a member of the overlay when created (the tool listed it as "reached" rather than a pre-declared member), since I only added it after seeing the full row list under `sec-hard-perdiem`.
