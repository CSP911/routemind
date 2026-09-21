1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Consultant one-time engagement ~3M won: whose signature, and are multiple quotes required?" --member /v1/regions/procurement "approval threshold by amount/category/term, likely covers one-time service procurement and quote requirements"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m1/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f3da23 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m1/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**
The team lead signs it off. Yes — two competing quotes are required. (Delegation limit for this row is 5,020 thousand KRW; expect 5 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m1/body

4. **Notes**
"A consultant's time" maps to category C2 only via the category legend's literal wording ("a consultant's time" is the exact example given) — no guessing needed there. "Roughly 3 million won" and "just the once" likewise matched the amount (V2) and term (M1) legend entries word-for-word, so classification was unambiguous. The one place I deliberately slowed down was the threshold table itself: it warns up front that this subject has been written three times (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) and that reaching for the newest is wrong for dates before 2026-01-01. I checked the revision legend explicitly rather than assuming "current" was right, since today's date (2026-09-21) is late in the year and it would have been easy to skip that check. It confirmed the 2026-01-01-onwards table is correct here. No other ambiguity — the row named exactly one signer and one quote count.
