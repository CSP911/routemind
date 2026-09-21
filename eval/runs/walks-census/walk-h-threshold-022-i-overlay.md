1. Commands:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, around 12 million won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches laptops purchase with 3-year lock-in and signature/quote question"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f413f7 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body

2. Answer:
The division director signs it off, and yes — three competing quotes are required. (Delegation limit for this row is 20,010 thousand KRW, so 12 million won falls within it.)

3. Source:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body

4. Notes:
The legends map each part of the question to a code with no rounding needed: "a couple of laptops" is the literal example given for category C1, "around 12 million won" is the literal example given for amount V3, and "locked in for three years" is the literal example given for term M3 — so the row lookup (C1/V3/M3) was unambiguous, no nearest-entry judgment call required.

The one place I nearly went wrong: the sec-hard-threshold table's description says it is "in force from 2026-01-01" and its own listing warned of a legend-revision file noting three historical versions of this table (v2 covering 2024-07-01 to 2025-12-31, and an older `threshold-table` before that). Today's date is 2026-09-21, so the 2026-01-01 table is current and correct, but I did not open the revision-legend or the superseded v2 row — worth flagging that I trusted the "in force from" date on the table header rather than cross-checking the revision legend explicitly. Given the date is well past 2026-01-01 with no later version listed, this should be safe.
