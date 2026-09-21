1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C2, amount V4, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, likely has the C2/V4/M1 lookup" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions, need to confirm which is in force today (2026-09-21)" --member /v1/nodes/purchase-request "may cover how many quotes needed before approval"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_869721 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body

2. **Answer**:
Signature: the department head signs it off.
Other prices: yes — three competing quotes and a written comparison are required first.
(Also: delegation limit 100,028 thousand KRW; 11 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions is in force for today's date, 2026-09-21)
- /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body (the actual row: signer, quotes, delegation limit, timeline)

4. **Notes**:
The procurement region table lists a superseded `hard-threshold-v2` file right alongside the current `sec-hard-threshold` table, with no date called out in the region-table listing itself — easy to grab the wrong one if you don't first check the legend-revision page. That page spells out the trap explicitly: for a 2025-dated question the answer is the *middle* version, not the oldest or the newest, so "always take the current table" is the wrong reflex to build. Since today is 2026-09-21, the current table (`sec-hard-threshold`, in force since 2026-01-01) was correct here, but I read the legend first rather than assuming.

The overlay itself never had `sec-hard-threshold` expanded into individual C/V/M rows as a directly-added member — the tool auto-expanded it into all 4×4×4 row files under that member when the overlay was created, which is how the exact `c2-amount-v4-term-m1` row appeared without me having to enumerate it. The close output flagged the row as "reached" rather than a named member, which just reflects that I read it via the expanded listing rather than adding it explicitly — the citation is otherwise exact and unambiguous.

No other area (expense/attendance/approval/payroll) was relevant; procurement's approval-threshold table was the only plausible source and it resolved cleanly to one row.
