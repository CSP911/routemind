1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body

2. **Answer**
Accrues 1.06 days per month. Carry-over limit is 5 days — that is the most that can still be held into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body

4. **Notes**
The leave accrual subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns that reaching for the newest table is wrong for any date before 2026-01-01. Today is 2026-09-20, so the current table (`sec-hard-accrual`, in force from 2026-01-01) is the right one — but this was a real branch point, not a formality, since the wrong pick would have silently returned a plausible-looking but superseded number.

The row is indexed by three qualifiers (type/tenure/site) that must each be translated from plain language via a separate legend file — "three days a week" → E3, "eight months" → T1, "Busan branch" → L2. None of these mappings are obvious or guessable; all three legends had to be read before the row address could be assembled correctly. It would have been easy to guess "part-time" language maps to a different code, or to assume tenure bands differently (e.g. treating 8 months as under a 1-year threshold rather than matching the literal "eight months" row) — but the legend gives literal example phrases as its left column, not numeric thresholds, so exact phrase matching against the legend rows was the safer read.

"How much can I still be holding in January" is answered by the carry-over limit field (5 days), reading January as the start of the new leave year following accrual — the table doesn't separately break out a "January-specific" cap, so this is the natural reading of the field but is an interpretive step worth flagging.
