1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "29 June 2024 overtime multiplier beyond 40-hour week (version in force that day)" --member /v1/regions/payroll "overtime multiplier likely defined in payroll rules"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/nodes/payslip-overtime
./bench/rmcli.py table /v1/nodes/payroll-desk
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py table /v1/nodes/overtime-rate-table
./bench/rmcli.py overlay add --id ov_2026-09-20_5651a8 --address /v1/nodes/hard-overtime-legend-revision/body --why "confirms three versions exist and which date range each covers"
./bench/rmcli.py overlay add --id ov_2026-09-20_5651a8 --address /v1/nodes/overtime-rate-table/body --why "the oldest version, in force until 2024-07-01, covers 29 June 2024"
./bench/rmcli.py overlay remove --id ov_2026-09-20_5651a8 --address /v1/nodes/hard-moved-overtime/body --why "wrong changepoint (2026-01-01), not the one relevant to 2024-06-29"
./bench/rmcli.py overlay close --id ov_2026-09-20_5651a8 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/overtime-rate-table/body

2. **Answer**: +50% (a 1.5x multiplier) for ordinary overtime beyond the 40-hour week.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body (used to identify which of three versions is in force on 2024-06-29)
/v1/nodes/overtime-rate-table/body (the version in force until 2024-07-01, which is the answer's source)

4. **Notes**: The obvious first hit is payroll's `payslip-overtime` document, which also states +50% for overtime beyond the standard week and carries no warning about being outdated (it's flagged only as superseded from 2026-01-01 onward by `hard-moved-overtime`). It would have been easy to stop there and answer +50%, arriving at the right number for the wrong reason. But the question's own framing ("two days before the first change") signals there were at least two change dates, not one — and `hard-moved-overtime` only documents a single changepoint (2026-01-01). That mismatch is what sent me to check attendance, where `hard-overtime-legend-revision` reveals a second, earlier revision on 2024-07-01 that payroll's own pages never mention. The true source for 29 June 2024 is the oldest version, `overtime-rate-table`, reached only via the attendance legend page — payroll's copy of the same rule (`payslip-overtime`) is silent about this earlier split and would have given the same numeric answer coincidentally, masking the fact that the wrong document was used. The rate happens to be identical (+50%) across old and new versions here, so the multiplier itself didn't change, but the path to a defensible answer required finding the version-aware legend, not just the first plausible-looking table.
