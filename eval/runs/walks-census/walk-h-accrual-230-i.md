1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body

2. **Answer**
Accrues 1.28 days of leave per month. Carry-over limit is 13 days — that is the most you can still be holding at the start of January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body

4. **Notes**
The leave-accrual subject has three superseded/current versions keyed by date (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the revision-legend page is explicit that grabbing the newest without checking the date is wrong. Today is 2026-09-20, which is safely inside the current table's 2026-01-01-onward range, so no ambiguity there — but it would have been easy to skip that check and just take whichever table showed up first.

The three qualifiers (employment type, tenure band, site) are each resolved by a separate legend file rather than being guessable from the user's wording: "three days a week" maps to type E3 (not obviously "part-time"), "nine years" maps to tenure T4 (the top band, not a literal "9"), and "Seoul office" maps to site L1. Each legend also has a fallback rule ("take the nearest entry above it") for values not listed, which wasn't needed here since all three inputs matched exactly — but it's a trap if you assume no match means "not found."

The question's second half ("how much can I still be holding in January") is not phrased as a standard HR term. I read it as asking for the carry-over limit (13 days) — the maximum balance retained across the year boundary — rather than a projected balance, since the row's own field is literally labeled "Carry-over limit, days" and no other field in the row or table fits "holding in January" better.
