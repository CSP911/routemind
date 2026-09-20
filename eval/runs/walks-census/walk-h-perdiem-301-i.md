## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/regions/expense
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
    ./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body
    ./bench/rmcli.py table /v1/nodes/evidence

## Answer

Lodging cap: 291 USD per night. Receipt required above 33 USD.

(Managing director → grade G4, Tokyo → band B1, four nights → stay S2, current table in force since 2026-01-01.)

## Source

- /v1/nodes/hard-perdiem-legend-revision/body (established today's date puts this under the current, 2026-01-01-onward table, not either older version)
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → G4)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → B1)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → S2)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body (the figures)

## Notes

- Overseas per-diem has three superseding versions living side by side under different addresses (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the oldest never says it was replaced — the legend-revision page is the only thing that flags this, and it's easy to walk straight past it to the table listed first (`sec-hard-perdiem`) without checking that today's date (2026-09-20) actually falls in its range. It does, but that was a check worth making rather than assuming.
- "Four nights" maps exactly onto stay S2 with no rounding needed — a case where nearest-entry guessing wasn't required, but the legend has to be read every time since the boundaries (one night / four nights / eight nights / three weeks) aren't obvious from the grade alone.
- The per-diem row itself carries its own "Receipt threshold" figure (33 USD), separate from lodging/meals/incidentals. I checked the general `evidence` table to see if a broader, conflicting receipt rule existed, but it covers evidence *format* (tax invoice vs. card slip), not a threshold amount, so the per-diem row's figure stands as the answer without needing to merge anything from there.
