1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Junior analyst, Tokyo, 4 nights: hotel per-night cap and receipt requirement threshold" --member /v1/regions/expense "hotel spend caps and receipt requirements are business trip expense rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a39dbe --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body
```

2. **Answer**
Hotel (lodging) cap: 99 USD per night. Receipt required for any single item above 21 USD (the row's "Receipt threshold").
(Grade mapping used: junior analyst → G1, Tokyo → band B1, four nights → stay S2, current table in force from 2026-01-01.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies for today's date, 2026-09-21 → the current one)
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → B1)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → S2)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body (the figures: lodging 99 USD/night, receipt threshold 21 USD)

4. **Notes**
- The trap here is the per-diem versioning: `hard-perdiem-legend-revision` warns there are three separate per-diem documents (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) and that reaching for the newest is only correct if the question date actually falls after 2026-01-01. Today is 2026-09-21, so the current table (`sec-hard-perdiem`) is right, but it would have been easy to skip that check and just grab whichever per-diem node showed up first in the expense overlay — the overlay listed both `hard-perdiem-v2` (superseded) and the current table side by side with similar-looking names.
- The three qualifiers (grade, band, stay) are each resolved by a separate legend document, not guessable from the question wording — "junior analyst," "Tokyo," and "four nights" only map to G1/B1/S2 because each legend table says so explicitly. Nothing about this was inferable without reading all three legends.
- "Receipt threshold" in the row is the same figure as "above what amount do I have to keep the receipt" — this is stated directly in the row body, no separate lookup in the general `evidence` node was needed, though that node exists and could add general context if asked about receipts more broadly.
- The overlay close reported all five addresses as "reached... from somewhere the overlay never named" rather than as declared members — I read them via `table`/`read` directly rather than first adding each as an explicit overlay member, so they weren't formally tracked as overlay members even though they were the addresses actually used.
