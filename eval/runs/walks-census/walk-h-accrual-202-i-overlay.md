1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 8 months tenure, Singapore entity: monthly leave accrual and max carry-forward into January" --member /v1/regions/attendance "leave accrual and carry-forward rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py overlay add --id ov_2026-09-20_e0fe97 --address /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body --why "resolved row: E3=3 days/week, T1=8 months tenure, L3=Singapore entity"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e0fe97 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body

2. **Answer**
Accrues 1.08 days of leave per month. The carry-over limit is 6 days — that is the most you can still be holding once January starts; anything accrued beyond that cap that wasn't approved in advance is settled at the cap and the excess is not recoverable.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body

4. **Notes**
The main hazard here was the version trap: `sec-hard-accrual-legend-revision` warns leave accrual has three separate versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) and explicitly says reaching for the newest is wrong for a question dated before 2026-01-01. Today is 2026-09-20/21, so the current table (`sec-hard-accrual`, in force from 2026-01-01) is correct — but it would have been easy to skip that check and grab whichever row looked right. The three qualifiers (type/tenure/site) also aren't self-evident from the question's wording — "three days a week" reads like a schedule detail, not an employment-type code, and each legend table warns it is "the only place the mapping is written down," so guessing without reading all three legends would risk a wrong row. All three qualifiers happened to match a legend entry exactly (E3, T1, L3), so no nearest-neighbor judgment call was needed here. The row itself bundles accrual and carry-over into one document, so no second table lookup was needed once the row was found.
