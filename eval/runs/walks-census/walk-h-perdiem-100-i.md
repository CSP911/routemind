1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
```

2. **Answer**
For a team manager (grade G2) on a one-night trip (stay S1) to Tokyo (band B1), under the per-diem table in force since 2026-01-01:
- Lodging cap: **159 USD per night**
- Receipt required above: **22 USD** (the receipt threshold)

(For reference, the same row also lists meals at 47 USD/day and incidentals at 9 USD/day, though these weren't asked for.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body — mapped "team manager" → G2
- /v1/nodes/hard-perdiem-legend-band/body — mapped "Tokyo" → B1
- /v1/nodes/hard-perdiem-legend-stay/body — mapped "one night" → S1
- /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body — the figures
- /v1/nodes/hard-perdiem-legend-revision/body — confirmed today's date (2026-09-20) falls under this current table, not the superseded v2 or original overseas-rates

4. **Notes**
The /v1/regions/expense table surfaces three per-diem documents at once: a legend-revision warning, a superseded `hard-perdiem-v2` file, and the current `sec-hard-perdiem` table — it would be easy to grab the wrong one without reading the revision warning first. The revision doc makes clear the date on the question (not just "use the newest") decides the version, and that the oldest version doesn't self-identify as superseded. Since today is 2026-09-20 (after 2026-01-01), the current table applies here, but this is exactly the kind of question where a 2025-dated version of the same request would need `hard-perdiem-v2` instead. No ambiguity in the grade/band/stay mappings — "team manager", "Tokyo", and "one night" are all listed verbatim in their respective legends.
