## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body

## Answer
The division director signs it off. Yes — three competing quotes and a written comparison are required before signoff. (Delegation limit for this row is 100,046 thousand KRW; expect 13 working days.)

## Source
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body

## Notes
The procurement table flags up front that the approval-threshold subject has three versions with overlapping-looking scope, and that reaching for the newest is wrong for dates before 2026-01-01 — that's the trap this walk is built to catch. Today's date (2026-09-21) falls under the current table (`sec-hard-threshold`, in force from 2026-01-01), so no correction was needed here, but I checked the legend-revision page explicitly rather than assuming, since the same question dated in 2025 would have needed `hard-threshold-v2` instead. The three qualifiers (category/amount/term) each have their own legend page mapping plain-language descriptions to codes ("flights and hotels" → C3, "about 40 million won" → V4, "locked in for three years" → M3); skipping any one of those legends and guessing the row address would have been the other easy way to go wrong, since row addresses are not derivable except by reading all three legends first.
