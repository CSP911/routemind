## Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body

## Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.

(Row selected: origin O2 = "a firm in Stuttgart", value W3 = "three hundred million won", goods K3 = "people's time". Screening score required: 56; financial statements: last two years — given for context, not asked.)

## Source

- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → O2)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → W3)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → K3)
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body (site visit: yes; re-review interval: every 12 months)

## Notes

- The procurement area lists a `supplier-due-diligence` page and a `sec-hard-diligence` table separately, plus explicit "v2" and "legend-revision" pages warning that due diligence rules have THREE overlapping versions. The generic `supplier-due-diligence/body` page (the pre-2026-01-01 "three checks" narrative) does not mention site visits or re-review cadence at all — reading only that page would have produced a false "not found." The real figures live one level deeper, in the current (2026-01-01–onward) indexed table `sec-hard-diligence`, keyed by origin/value/goods codes.
- All three legend tables state "If what you have is not listed, take the nearest entry above it" — not needed here since all three phrases in the question ("a firm in Stuttgart," "three hundred million won," "people's time") are exact, verbatim matches to legend rows, so no nearest-neighbor judgment call was required.
- Did not open `hard-diligence-v2` or `hard-diligence-legend-revision` — today's date (2026-09-20) falls inside the current table's stated force period (from 2026-01-01), so the superseded version was irrelevant. Worth flagging only because the warning text is alarming enough that it's tempting to go check the older version "just in case"; the row itself already states its own in-force date, which is sufficient.
