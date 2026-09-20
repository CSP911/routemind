1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s2/body
./bench/rmcli.py table /v1/nodes/evidence

2. **Answer**
Lodging (hotel), per night: 307 USD.
Receipt required above: 42 USD.
(Managing director = grade G4, Singapore = band B2, four nights = stay S2, current table in force since 2026-01-01.)

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s2/body

4. **Notes**
- The expense area's table listing flags up front that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem` effective 2026-01-01). It would be easy to grab the wrong version's row by habit; I confirmed via the row's own "in force from 2026-01-01" footer that this is the one that applies to today's date (2026-09-20), and did not open the two older versions since the current one already answered the question.
- The per-diem table is indexed by three separate legends (grade, band, stay) rather than one lookup — the row address itself (`...-row-grade-g4-band-b2-stay-s2`) has to be assembled from three independent translations (job title → grade, city → band, trip length → stay). It would be easy to guess at an address instead of reading all three legends; the instructions explicitly forbid constructing addresses, and here it mattered because "four nights" maps exactly onto "stay S2" with no rounding needed, but a slightly different night count would require the "nearest entry above it" fallback stated in each legend.
- I opened the general `/v1/nodes/evidence` table to check whether a separate, broader receipt rule might override or contextualize the per-diem row's own "Receipt threshold" field, but nothing there was needed to answer the question — the per-diem row states its own threshold directly, so I did not descend further into it.
