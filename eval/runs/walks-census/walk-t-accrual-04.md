1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body

2. **Answer**: 0.50 days per month (monthly accrual rate for type E2, tenure/service band T2, under the version in force 2024-07-01 to 2025-12-31).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (identifies which version applies to October 2024)
- /v1/nodes/hard-accrual-v2/body (the rate table itself: E2 × T2 = 0.50)

4. **Notes**: Leave accrual has three separately-written versions with overlapping-looking scope, and the attendance table lists both `hard-accrual-v2` and `sec-hard-accrual` ("THE CURRENT LEAVE ACCRUAL TABLE") side by side with no date in the row description for the former — it would be easy to grab the current table (`sec-hard-accrual`, in force 2026-01-01 onward, 3 qualifiers including site) by mistake, which is exactly the trap the legend page warns about. The legend page explicitly says October 2024 falls in the 2024-07-01–2025-12-31 window, so `hard-accrual-v2` is correct, not the current table and not the oldest (`leave-accrual`, pre-2024-07-01, no type/site breakdown). One ambiguity I couldn't resolve from the source: the table gives a monthly accrual *rate*, not a total; the question asks "how much was accrued... in October 2024," which I read as one month's accrual (0.50 days), not a year-to-date total — the document doesn't state a separate one-time "granted" figure distinct from the monthly rate.
