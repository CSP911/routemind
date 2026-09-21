1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Dhaka, 3-week trip: nightly hotel cap and receipt threshold?" --member /v1/regions/expense "business trip pay / hotel per diem and receipt rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2dc00d --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body
```

2. **Answer**
Nightly hotel (lodging) cap: 283 USD per night. Receipt required above: 62 USD (the receipt threshold). This is from the current overseas per-diem table (grade G3 / band B4 / stay S4), in force from 2026-01-01.

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed today's date, 2026-09-21, falls under the current 2026-01-01-onward version, not the superseded ones)
- /v1/nodes/hard-perdiem-legend-grade/body ("department head" → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body ("Dhaka" → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body ("three weeks" → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body (the figures: lodging 283 USD/night, receipt threshold 62 USD)

4. **Notes**
The domain has three separate versions of the overseas per-diem document (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the oldest one gives no indication it was ever superseded — nothing in it points forward. Without deliberately reading the `hard-perdiem-legend-revision` warning page first, it would have been easy to land on the wrong version, especially since a table listing could surface any of the three depending on how it's searched. Today's date (2026-09-21) put the trip clearly in the current (2026-01-01+) version, so no real ambiguity here, but the walk-in-workspace explicitly flagged that a 2025-dated question would need the *middle* version, not the newest — a trap worth remembering for other per-diem questions. The three qualifiers (grade/band/stay) each required a separate legend lookup rather than being guessable from the question's wording ("department head" → G3, "Dhaka" → B4, "three weeks" → S4), and the row address is only constructible after all three are resolved — I did not guess or build the address, I read it off the table listing after computing the codes.
