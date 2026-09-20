## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body

## Answer
Accrues 1.58 days per month. Carry-over limit into January is 13 days.

(Row selected: type E4 "here from our partner firm", tenure T3 "been here five years", site L4 "fully from home" — all three qualifiers matched the legends verbatim, no nearest-entry judgment calls needed.)

## Source
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions is current for today's date, 2026-09-20)
- /v1/nodes/hard-accrual-legend-type/body
- /v1/nodes/hard-accrual-legend-tenure/body
- /v1/nodes/hard-accrual-legend-site/body
- /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body (accrual rate and carry-over figure)

## Notes
The main hazard here was version drift, not the lookup itself: `/v1/regions/attendance` lists three
separate accrual pages (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no version marker
visible until you open the legend-revision page. Grabbing the first plausible-looking accrual table
without checking dates would have been wrong for any question dated before 2026-01-01. For today's
date (2026-09-20) the current table (`sec-hard-accrual`, three qualifiers) is correct, but this is a
trap worth flagging.

The three qualifier phrases in the question mapped exactly onto legend rows with no ambiguity — "here
from our partner firm" = E4, "been here five years" = T3, "fully from home" = L4 — so no nearest-entry
substitution was needed, which is unusual for these tables and worth noting precisely because it means
there was no judgment call to second-guess.

One remaining ambiguity: "how much can I still be holding in January" was read as the carry-over limit
(13 days) — the cap on days that survive into the new year — rather than a projection of accrued-minus-used
balance by a specific January date, since no current balance or usage was given in the question and no
such projection is computable from this table alone.
