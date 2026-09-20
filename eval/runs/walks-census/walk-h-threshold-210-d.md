1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body

2. **Answer**: For category C3, amount V2, term M1 (delegation limit 5,036 thousand KRW), the **team lead** signs it off. Yes — two competing quotes are required before approval.

3. **Source**: /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body (row itself, current table in force from 2026-01-01), confirmed as the correct version via /v1/nodes/hard-threshold-legend-revision/body (today, 2026-09-20/21, falls under the current table `sec-hard-threshold`, not the superseded `hard-threshold-v2` or `threshold-table`).

4. **Notes**: The main risk here was version confusion — the procurement area lists THREE separate versions of the approval threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) all still live and none marked withdrawn, with an explicit warning that the oldest doesn't admit it's been superseded. I checked the legend-revision page before trusting the current table, which confirmed today's date falls in the 2026-01-01-onward range for `sec-hard-threshold`. Had I skipped that check and just grabbed the first threshold row I saw, I could easily have pulled from the wrong version, since the older two use their own row-address schemes and could plausibly look current at a glance. The row itself directly answered both parts of the question (signer = team lead; quotes = two) without needing to consult the legend-amount/category/term pages, since the question already gave codes (C3/V2/M1) rather than plain-language descriptions.
