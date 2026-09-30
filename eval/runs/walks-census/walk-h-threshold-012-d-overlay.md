1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V2, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - directly matches question" --member /v1/regions/approval "signature/approval chain info might live here too"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_49a9f2 --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body

2. **Answer**:
For category C1, amount V2, term M3: the department head signs it off. Yes, you need other prices first — two competing quotes are required. (Delegation limit for this row is 5006 thousand KRW; working days to expect is 7.)

3. **Source**:
/v1/nodes/sec-hard-threshold (table locating the row)
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m3/body (the row itself, answer taken from here)

4. **Notes**:
The first table listed both `/v1/regions/procurement` and `/v1/regions/approval` as plausible homes for "whose signature do I need" — approval sounds like it belongs to the Documents & Approval area. I kept both as overlay members to avoid committing early. Procurement's own region table warns explicitly that "approval thresholds by category, amount, term" live there, and the approval region even has a node (`hard-moved-threshold`) flagging that spend approval thresholds moved to procurement on 2026-01-01 — so approval would have been a dead end for this specific question. There's also a version trap: `sec-hard-threshold` is explicitly the current table (in force from 2026-01-01), with `hard-threshold-v2` (2024-07-01 to 2025-12-31) and an unnamed older `threshold-table` as superseded versions, plus a `hard-threshold-legend-revision` warning node about three versions existing. Today's date (2026-09-21) falls inside the current table's validity window, so I used it directly and didn't need to open the superseded versions — but it would have been easy to grab a stale row by address pattern-matching without checking the in-force dates first.
