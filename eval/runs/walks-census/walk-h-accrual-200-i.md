1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body

2. **Answer**
Accrual: 1.04 days per month.
Carry-over limit into January: 4 days maximum can still be held.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body

4. **Notes**
The accrual subject has three superseded/current versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) keyed by date, and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so no ambiguity there — but it would have been an easy trap on an older-dated question since the oldest version "says nothing at all about having been replaced."

The three qualifiers (type, tenure, site) each needed their own legend to translate the plain-language description into a row code, and each translation happened to land on an exact match rather than a "nearest entry" judgment call: "three days a week" → E3, "eight months" → T1, "Seoul office" → L1. Worth flagging that if any of those phrasings had been slightly off (e.g. "about eight months" or "mostly in Seoul"), the legends explicitly allow falling back to the nearest listed entry, which would have been a genuine judgment call rather than a lookup.

The phrase "how much can I still be holding in January" maps to the row's "Carry-over limit, days" field (4), not the monthly accrual rate — the wording doesn't use the term "carry-over" so this took a beat to connect. The row's "If the figures are exceeded" section (unapproved excess forfeited, unavoidable excess needs written justification to the budget holder) wasn't asked about but is adjacent and was left out of the answer since it wasn't requested.
