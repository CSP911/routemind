1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 5 years tenure, Seoul office: monthly leave accrual rate and max carryover/holding cap in January" --member /v1/regions/attendance "leave accrual and carryover rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py overlay add --id ov_2026-09-20_73af1e --address /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body --why "resolved row: partner firm=E4, five years=T3, Seoul office=L1"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_73af1e --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body

2. **Answer**
Accrues 1.52 days per month. The carry-over limit (the most you can still be holding into January) is 10 days.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body

4. **Notes**
The three-version warning (`hard-accrual-legend-revision`) was the sharpest fork in the walk: leave accrual has three superseded/current tables indexed by date, and grabbing the newest without checking would be wrong for a question dated before 2026-01-01. Today is 2026-09-20/21, so the current table (`sec-hard-accrual`, in force from 2026-01-01) is the right one — but this is exactly the trap the legend page calls out.

Translating the question's phrasing into row qualifiers required all three legends, not just the tenure one. "Here from our partner firm" isn't an obvious synonym for "type E4" until you read the type legend — I initially assumed "partner firm" might mean a contractor (type E2, "on a two-year contract") but the legend's own wording ("here from our partner firm") is a near-verbatim match for E4, so I went with that instead. "Been here five years" matches tenure T3 exactly (no interpolation needed), and "the Seoul office" matches site L1 exactly. All three were exact matches, not nearest-neighbor guesses, which is worth flagging since the legends explicitly allow falling back to "the nearest entry above" when there's no exact match — that fallback wasn't needed here.

The question's "how much can I still be holding in January" reads like it could be asking about something month-specific (e.g., a use-it-or-lose-it deadline tied to January), but the row's data model only has a flat "carry-over limit" figure (10 days) with no month-specific variation — that single number is what answers "holding in January."
