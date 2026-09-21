1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In October 2024, what screening was required for an origin O2 supplier at contract value W2? Answer under the version of supplier due diligence that was in force on that date." --member /v1/regions/procurement "supplier due diligence / screening by origin and contract value would be under procurement policy"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-v2
./bench/rmcli.py table /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5fa734 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-v2/body

2. **Answer**:
Screening score required = **35**, for origin O2 at contract value W2, under the version of supplier due diligence in force 2024-07-01 to 2025-12-31 (which covers October 2024). The other elements of the row (documents to collect, re-review interval) were not varied by this version and followed the pre-2024-07-01 rule unchanged.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established there are three versions of supplier due diligence and which date range each covers)
- /v1/nodes/hard-diligence-v2/body (the version in force 2024-07-01 to 2025-12-31; O2×W2 cell = 35)

4. **Notes**:
The near-miss here was reaching straight for `sec-hard-diligence`, the table procurement's overview lists as "THE CURRENT SUPPLIER DUE DILIGENCE TABLE" — it's the first and most prominent due-diligence table in the working set, and it does have an O2/W2 row (under goods K1-K4), but it's the 2026-01-01-onwards version and doesn't even apply to October 2024. The legend-revision page exists specifically to stop that mistake and makes clear this question falls in the *middle* version (`hard-diligence-v2`), not the newest and not the oldest — explicitly called out as "the case worth being careful about."

The other point of friction: `hard-diligence-v2`'s table gives bare numbers (30–45) with no legend of its own explaining what they mean. I confirmed the meaning by checking the current table's per-row format, which labels the equivalent number "Screening score required" — the v2 table is structured identically (origin × value matrix of the same kind of figure), just condensed into one page instead of per-row pages, since v2 predates the three-qualifier (origin/value/goods) split and only had two qualifiers.
