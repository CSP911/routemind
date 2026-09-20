1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/nodes/payslip-overtime
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
```

2. **Answer**
Two versions are needed:

- **2023 claim → `overtime-rate-table`** (in force until 2024-07-01): ordinary overtime paid at **+50% (1.5x)** of the hourly basic pay rate, flat — one qualifier, no day/hour breakdown.
- **2025 claim → `hard-overtime-v2`** (in force 2024-07-01 to 2025-12-31): ordinary overtime paid on a **day × hours matrix, from 1.20x up to 1.65x**, indexed by day tier (D1–D4) and hour tier (H1–H4):

  | day \ hours | H1 | H2 | H3 | H4 |
  |---|---|---|---|---|
  | D1 | 1.20x | 1.23x | 1.26x | 1.29x |
  | D2 | 1.32x | 1.35x | 1.38x | 1.41x |
  | D3 | 1.44x | 1.47x | 1.50x | 1.53x |
  | D4 | 1.56x | 1.59x | 1.62x | 1.65x |

  Which specific day/hour tier applies to a given claim is not stated in this document — this table only gives the schedule of multipliers, not the mapping from a claim's actual hours to D1–D4/H1–H4.

3. **Source**
- /v1/nodes/hard-overtime-legend-revision/body (routing table — names the three versions and which dates each covers)
- /v1/nodes/overtime-rate-table/body (2023 rate — until 2024-07-01)
- /v1/nodes/hard-overtime-v2/body (2025 rate — 2024-07-01 to 2025-12-31)

4. **Notes**
- The obvious first path is wrong: the payroll region's `hard-moved-overtime` page says overtime premiums moved to attendance on 2026-01-01 and that "the old rule" still in payroll is `payslip-overtime`. Since both 2023 and 2025 predate 2026-01-01, it looks like `payslip-overtime` (flat +50%/+50%/+50%/+100% by overtime/night/holiday-first-8h/holiday-beyond-8h) should answer both claims. That is a trap: `payslip-overtime` carries no effective-date range at all and never appears in the actual version ledger. Taking it at face value would have given one wrong flat answer for both years.
- The real version history only surfaces in the attendance region, under `hard-overtime-legend-revision`, which explicitly warns that this subject "has been written three times" and that the oldest version "says nothing at all about having been replaced" — which is exactly the trap `payslip-overtime` sets, except the legend is talking about `overtime-rate-table`, not `payslip-overtime`. It would be easy to conflate the two silent-about-replacement documents; they are not the same document and not indexed the same way (one qualifier vs. two).
- The legend page gives ids, not addresses (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) — had to find `overtime-rate-table`'s real address by opening `sec-overtime-and-hours` in attendance rather than constructing a path from the id.
- The legend explicitly calls out 2025 as "the case worth being careful about: it is the one where taking either extreme is wrong" — i.e. neither the oldest table nor the current (2026-01-01+) `sec-hard-overtime` table answers a 2025 claim; only the middle version (`hard-overtime-v2`) does. 2023, by contrast, needs the oldest table, `overtime-rate-table`.
- `hard-overtime-v2` gives a multiplier matrix rather than a single number, and does not itself define what makes an hour "D2" vs "D3" or "H1" vs "H3" — reconciling an actual 2025 claim would need that mapping from elsewhere, which this walk did not chase down since it wasn't asked for.
