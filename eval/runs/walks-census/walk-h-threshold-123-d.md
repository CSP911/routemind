1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body

2. **Answer**:
For category C2, amount V3, term M4 (delegation limit 20,027 thousand KRW): the division director signs it off. Yes, other prices must be obtained first — three competing quotes are required. (11 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies for 2026-09-20)
- /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body (the answer)

4. **Notes**:
The procurement area warns up front that approval-threshold content exists in THREE versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and that the oldest version says nothing about being superseded — so grabbing the first plausible-looking row without checking the legend-revision page would silently give a stale answer. Today's date (2026-09-20) is comfortably inside the current version's range, so this case wasn't the tricky one the warning specifically calls out (that's for 2025-dated questions, which need the middle version), but the check was still necessary to be sure. The current table (`sec-hard-threshold`) is indexed by three qualifiers (category/amount/term) and had an exact row matching C2/V3/M4, so no interpolation or legend lookups for the qualifier definitions were needed since the question already gave the codes directly.
