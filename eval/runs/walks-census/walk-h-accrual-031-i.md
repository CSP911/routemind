1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body

2. **Answer**: Accrues 0.66 days per month. Carry-over limit is 14 days (the most that can be held into January).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirms current table applies for a 2026-09-20 question)
- /v1/nodes/hard-accrual-legend-type/body (regular payroll → type E1)
- /v1/nodes/hard-accrual-legend-tenure/body (nine years → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body (Busan branch → site L2)
- /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body (0.66 days/month, 14-day carry-over limit)

4. **Notes**: The attendance area lists three separate versions of the leave accrual table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page warns that reaching for the newest is only correct if the question's date actually falls in that window — with today at 2026-09-20 the current table (`sec-hard-accrual`) is right, but it would have been an easy mistake to grab it without checking the date, or conversely to second-guess and pull the superseded `hard-accrual-v2`. The three qualifiers (employment type, tenure band, site) each have their own legend page that must be read literally — "regular payroll," "nine years," and "Busan branch" are exact matches to legend rows here (E1, T4, L2), so no nearest-entry judgment call was needed. The row itself bundles accrual rate and carry-over limit together, which directly answers both halves of the question from a single document.
