1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
```

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.

(This is the current supplier due-diligence table, in force since 2026-01-01, which applies to today's date, 2026-09-20. Row: origin O3 [Austin] / value W4 [seven hundred million won] / goods K4 [a licence]. That row also requires a screening score of 77 and audited financial statements for the last three years, though those weren't asked.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Austin → O3)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → W4)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → K4)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body (site visit: yes; re-review: every 6 months)
- /v1/nodes/hard-diligence-legend-revision/body (confirms current table applies for 2026-09-20)

4. **Notes**
- The procurement area table lists both a `sec-hard-diligence` (current, three-qualifier) table and older superseded versions (`hard-diligence-v2`, and the oldest `supplier-due-diligence`) side by side with no date filtering — it would be easy to grab the wrong version's row by picking the first "due diligence" table that looks plausible. The legend-revision page is explicit that the newest isn't always right ("reaching for the newest is wrong for anything before 2026-01-01"), so I checked it deliberately even though today's date made the current table the obvious right call.
- I initially opened `supplier-due-diligence/body` (the general narrative page under `sec-supplier-due-diligence`) expecting it to hold the on-site-visit/re-review answer since it discusses "the ongoing side of the same checks, re-run rather than one-off." It doesn't — that page only covers the sanctions/code-of-conduct/disqualification screen, not site visits or a review cadence. The real answer lives entirely in the indexed row table (`sec-hard-diligence`), not in the narrative overview pages. Worth flagging: the overview's "fourth page" phrasing is a bit of a red herring for this specific question.
- All three qualifiers (Austin, seven hundred million won, a licence) matched a legend row's left-hand column exactly — no nearest-match judgment call was needed, which removed one likely source of error.
