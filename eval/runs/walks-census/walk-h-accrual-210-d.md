1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body

2. **Answer**
Accrues 1.12 days per month. Carry-over limit is 7 days — that is how much you can still be holding in January (the rollover cap). (Notice required to use leave: 4 working days; does not accrue during unpaid leave.)

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body

4. **Notes**
The type/tenure/site codes were given directly in the question (E3, T2, L1), so no legend lookup was needed to translate plain-language qualifiers into codes — I went straight to the matching row in the 64-row table. The table listing at /v1/regions/attendance flagged that leave accrual has three superseded versions (via hard-accrual-legend-revision); I confirmed I was on the current one (`sec-hard-accrual`, in force from 2026-01-01) rather than accidentally reading `hard-accrual-v2` (2024-07-01 to 2025-12-31), which sits right next to it in the attendance table listing and could easily be grabbed by mistake. The only interpretive step was reading "how much can I still be holding in January" as the carry-over limit rather than a separate document — the row's own fields (accrual rate, carry-over limit) covered both parts of the question directly, so no second source was needed.
