1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body

2. **Answer**
Lodging cap: 131 USD per night. Receipt required above: 39 USD (the receipt threshold). This is for a junior analyst (grade G1), Jakarta (band B3), a four-night stay (stay S2), under the per-diem table in force since 2026-01-01.

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body

4. **Notes**
The expense area lists three overlapping versions of the overseas per-diem (a legend-revision warning, a superseded `hard-perdiem-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-perdiem` table for 2026-01-01 onward) — easy to grab the wrong one if you don't check dates against today (2026-09-20). I went straight for `sec-hard-perdiem` since it's explicitly marked current and today's date falls after 2026-01-01 with no end date given.

The per-diem table itself is indexed by opaque codes (grade/band/stay), and none of the 64 row addresses spell out "junior analyst," "Jakarta," or "four nights" — you have to detour through three separate legend files to translate the plain-language question into G1/B3/S2 before the row address even makes sense. Skipping any one of the three legends risks silently reading the wrong row (e.g. confusing Jakarta's band B3 with Singapore's B2, or four nights' S2 with one night's S1).

The "receipt threshold" figure sits inside the same per-diem row as the lodging cap, not in the separate `/v1/nodes/evidence` table I initially expected to need — worth noting since a literal reading of the question ("above what amount do I have to keep the receipt") could send you looking in Evidence instead, when the number specific to this trip is actually per-diem-row-specific and lives here.
