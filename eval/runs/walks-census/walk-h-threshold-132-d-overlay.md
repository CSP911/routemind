1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C2, amount V4, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches question directly"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_397008 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body

2. **Answer**
For category C2, amount V4, term M3: the division director signs it off, and yes — three competing quotes plus a written comparison are required before signing (delegation limit 100,030 thousand KRW; 13 working days to expect). An excess not approved in advance is settled at this figure with the difference not recoverable; an unavoidable excess is claimed via written statement and decided by the budget holder.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies to today's date)
/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body (the answer itself)

4. **Notes**
The procurement region's overlay member list surfaced two current-vs-superseded pairs (hard-threshold-v2 vs sec-hard-threshold, and a matching pair for supplier due diligence) without saying outright which applies "now." The legend-revision page made clear there are three approval-threshold versions on different date ranges and that reaching for the newest without checking the date is explicitly called out as wrong for pre-2026 questions — today's date (2026-09-20) falls in the 2026-01-01-onwards window, so the current table (`sec-hard-threshold`) was correct, but this was a real branch point, not a formality: for a 2025-dated question the answer would have come from `hard-threshold-v2` instead. The sec-hard-threshold table then had an exact-match row for C2/V4/M3 (no need to interpolate from legends for category/amount/term bands), which made the final read unambiguous. The overlay close reported the two addresses I used as "reached... from somewhere the overlay never named" since I read them via the table drill-down rather than adding them as explicit overlay members — worth noting in case that's meant to be done differently.
