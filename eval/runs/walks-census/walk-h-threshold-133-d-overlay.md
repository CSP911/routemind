1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C2, amount V4, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term is exactly this row's domain"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0d760d --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body

2. **Answer**:
For category C2, amount V4, term M4: the CFO signs it off (delegation limit 100,031 thousand KRW). Yes, other prices are required first: three competing quotes plus a written comparison. Working days to expect: 14. This is the current table, in force from 2026-01-01, which covers today's date (2026-09-20/21).

3. **Source**:
- /v1/regions/procurement (entry point, led to the working set)
- /v1/nodes/sec-hard-threshold (confirmed this is THE CURRENT approval threshold table, in force from 2026-01-01, and located the exact row)
- /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body (the row with the answer)

4. **Notes**:
The procurement region table listed both a current table (`sec-hard-threshold`, in force from 2026-01-01) and a superseded version (`hard-threshold-v2`, 2024-07-01 to 2025-12-31), plus a "legend-revision" warning node saying there are three versions of this table total. It would have been easy to grab the superseded `hard-threshold-v2` by mistake since it sorted near the top of the results. I stuck with `sec-hard-threshold` because its description explicitly says "in force from 2026-01-01" and today's date (2026-09-20) falls inside that range, so I didn't need to open the legend-revision node to resolve ambiguity — the row itself also restates its own effective date and points back to the older versions, which matched. The category/amount/term row existed as an exact, single match (no need to consult the amount/category/term legends to map fuzzy inputs to codes, since C2/V4/M4 were already given as codes), which kept the walk short.
