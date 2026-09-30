1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Department head, Jakarta, one night — hotel per-diem cap and receipt threshold" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01" --member /v1/nodes/evidence "what has to be attached for a spend to be accepted — receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_1f1e40 --address /v1/nodes/sec-evidence-in-awkward-cases --why "not needed — no awkward-evidence case here"
./bench/rmcli.py overlay close --id ov_2026-09-21_1f1e40 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body

2. **Answer**
Lodging cap: 255 USD per night. Receipt is required above 44 USD (the per-diem row's own receipt threshold).
(For reference, same row also gives: meals 84 USD/day, incidentals 17 USD/day — not asked for, but adjacent.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed sec-hard-perdiem, in force 2026-01-01 onward, is the correct version for today's date)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body (the row: lodging 255 USD/night, receipt threshold 44 USD)

4. **Notes**
The near-miss was the receipt threshold: /v1/regions/expense also lists a general "qualifying evidence" table (/v1/nodes/qualified-evidence → qualified-list/body) with a receipt ceiling of 30,000 KRW. That table is for domestic/general expense evidence in KRW and is a different rule from the per-diem row's own "Receipt threshold" field (44 USD), which is denominated in USD and specific to this grade/band/stay combination on an overseas trip. Using the KRW figure here would have been wrong — the per-diem row carries its own receipt threshold precisely so you don't have to cross-reference the general evidence table for overseas trips. Also worth flagging: the per-diem table has three superseded versions (overseas-rates, hard-perdiem-v2, sec-hard-perdiem); I checked hard-perdiem-legend-revision to confirm the current one applies since the question is dated to today (2026-09-21), which is after the 2026-01-01 cutover — a question dated in 2025 would need hard-perdiem-v2 instead.
