1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body

2. **Answer**
Lodging cap: 251 USD per night. Receipt required above: 44 USD (receipt threshold).
(For reference, same row also gives meals 85 USD/day and incidentals 17 USD/day, but those weren't asked.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body

4. **Notes**
The expense area lists three versions of the overseas per-diem (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), with an explicit warning node about which dates each covers. It would have been easy to grab a superseded table by mistake — I went straight to `sec-hard-perdiem` because its description states it's in force from 2026-01-01, which covers today's date (2026-09-20), and skipped the older two entirely. The row address itself was printed exactly as `hard-perdiem-row-grade-g3-band-b2-stay-s4`, matching G3/B2/S4 with no ambiguity, so no legend lookup (grade/band/stay definitions) was needed since the question already gave the codes directly.
