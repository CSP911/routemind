1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Consultant's time, about 40 million won, locked in for three years: whose signature, and do I need other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches consultant service, amount, and 3-year term"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b2a2de --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body

2. **Answer**
This is category C2 (a consultant's time), amount V4 (about 40 million won), term M3 (locked in for three years). Row C2/V4/M3: signed off by the division director (delegation limit 100,030 thousand KRW). Yes, other prices are required first: three competing quotes and a written comparison. Expect about 13 working days.

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body

4. **Notes**
The procurement region table listed three versioned threshold tables (a "legend-revision" warning flagged this explicitly), so it would have been easy to grab the superseded `hard-threshold-v2` table instead. I used `sec-hard-threshold`, whose own description states it is in force from 2026-01-01, which covers today's date (2026-09-21), so it's the correct current table — no need to consult the legend-revision doc separately since the table's own header already gave the effective date. The three legend lookups (category/amount/term) were each unambiguous single matches, so no interpolation between banded values was needed.
