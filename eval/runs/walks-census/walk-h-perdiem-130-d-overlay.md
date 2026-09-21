1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G2, band B4, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel nightly cap and receipt threshold are expense-related figures"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_99ffee --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body

2. **Answer**: Lodging (hotel), per night: 207 USD. Receipt threshold: 49 USD (evidence must be kept/attached for spend above this amount). (For context, also on this row: meals 89 USD/day, incidentals 18 USD/day.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions applies for today's date)
- /v1/nodes/sec-hard-perdiem (table listing, confirmed the exact G2/B4/S1 row exists)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body (the answer itself)

4. **Notes**: The overseas per-diem subject has three superseded-but-not-marked-as-such versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 — the oldest version says nothing about being replaced, so skipping that check could silently give a stale answer. Today's date (2026-09-20/21) is safely inside the current table's validity (2026-01-01 onward), so `sec-hard-perdiem` was the correct pick, but this is exactly the kind of question where grabbing the first per-diem-looking node without checking the revision legend would go wrong for an older date. The row itself matched the three qualifiers (grade, band, stay) exactly with no interpolation needed. One minor mechanical note: the overlay only had `/v1/regions/expense` as a named member, so `overlay close --used` flagged the deeper addresses as "reached... from somewhere the overlay never named" — harmless, but worth adding sub-nodes as members earlier next time to avoid that flag.
