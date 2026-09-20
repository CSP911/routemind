## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body

## Answer
Multiplier: 1.71x. Rounding: to the nearest 5 minutes.

## Source
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body

## Notes
The attendance area lists three "hard-overtime" versions (a legend-revision file plus superseded
`hard-overtime-v2` and `overtime-rate-table`), so the first fork in the road is picking the right
vintage. The table description for `sec-hard-overtime` states outright it is "in force from
2026-01-01" and "replaces `overtime-rate-table`" and the older rules — since today is 2026-09-20,
that one is current and the other two are dead ends. Easy to miss if you jump straight to a row
from search without reading the table's own header.

The row addresses are pure codes (day D2, hours H1, place P2) with no plain-English meaning, so
guessing at a row without reading all three legends first would have been a coin flip — "Saturday"
isn't obviously D2 (D1 is an "ordinary Tuesday", D3 is a holiday, D4 is oddly a *time* — "two in the
morning" — mixed into what looks like a day-type column). Same trap on hours: "about ninety minutes"
matches H1 verbatim in the legend, so no rounding/interpretation was needed there, but it would have
been easy to instead reach for "H2 three hours" out of habit if skimming. Place was the cleanest
match: "out at a client's office" is copied almost word-for-word as P2 in the legend.
