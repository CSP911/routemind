1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G4, band B1, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01 - likely has hotel cap and receipt threshold" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of three per-diem versions with different date ranges - need to confirm which applies to today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_88bcde --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 291 USD per night. Receipt threshold: 33 USD (a receipt must be kept for any single spend above this amount). For reference, the same row also gives meals at 70 USD/day and incidentals at 14 USD/day.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (confirmed today's date, 2026-09-21, falls under the current 2026-01-01-onward table, not the two superseded versions)
/v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body (the figures)

4. **Notes**:
The expense area table flagged up front that overseas per-diem has three versions covering different date ranges, with the current one in force only since 2026-01-01 — that warning is what stopped me from just grabbing the first per-diem-looking row I saw. I deliberately pulled the revision legend into the working set alongside the current table before reading either, and confirmed today's date sits in the current range (three qualifiers: grade/band/stay) rather than the superseded `hard-perdiem-v2` or `overseas-rates`. Worth flagging: when I added `/v1/nodes/sec-hard-perdiem` as an overlay member, it expanded into every grade/band/stay row (64 of them) rather than just the one row I needed — the overlay tool only let me mark the specific G4/B1/S2 row as "reached" on close, not as a named member, since I never added it individually. No actual ambiguity in the final answer, just a slightly noisy working set.
