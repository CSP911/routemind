## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body

## Answer
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also: screening score required is 93, and audited financial statements for the last three years are required — not asked, but part of the same row.)

## Source
- /v1/nodes/hard-diligence-legend-revision/body (confirmed 2026-09-20 falls under the current, 2026-01-01-onwards version, not the superseded ones)
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body ("a licence" → goods K4)
- /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body (site visit: yes; re-review interval: every 6 months)

## Notes
- The procurement table lists three separate due-diligence eras (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with a dedicated legend-revision page warning that "the oldest says nothing at all about having been replaced" — it would have been easy to grab the wrong version by just picking the first plausible-looking due-diligence page instead of checking the date first. Today (2026-09-20) is safely inside the current table's range (2026-01-01 onwards), so no ambiguity there, but it's the kind of question where a 2025-dated question would need the middle version instead.
- "A licence" as a goods category is not obviously "a licence to operate/do business" vs. "software licence" — the legend just says "a licence" maps to K4 with no further qualification, so I took it at face value.
- The three qualifiers (origin, value, goods) had to be resolved independently via three separate legend pages before the row address could be built — none of the legends cross-reference each other, so it required three separate lookups before the final row read.
