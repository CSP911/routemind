1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 700M contract for custom-spec goods: is a site visit required, and how often is their vendor file reviewed?" --member /v1/regions/procurement "starting point for procurement/vendor questions"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_32a97a --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body

2. **Answer**
Yes, a site visit is required. The vendor's file must be re-reviewed every 6 months.
(Full row for reference: screening score required 59; financial statements last three years, audited.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body — established that today's date (2026-09-20/21) falls under the current table, not the two superseded versions
- /v1/nodes/hard-diligence-legend-origin/body — Stuttgart → origin O2
- /v1/nodes/hard-diligence-legend-value/body — seven hundred million won → value W4
- /v1/nodes/hard-diligence-legend-goods/body — "something made to our spec" → goods K2
- /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body — the row itself, giving "Site visit: yes" and "Re-review interval: every 6 months"

4. **Notes**
The supplier-due-diligence area has three versions in force over different date ranges, and the oldest one gives no indication it was ever superseded — the legend-revision doc warns explicitly that reaching for the newest table is wrong for a pre-2026 question, and reaching for the current table has to be a deliberate date check, not a default. With today dated 2026-09-20, the current table (`sec-hard-diligence`, in force from 2026-01-01) is the right one, but I only knew to check this because the working set surfaced the legend-revision file alongside the current and superseded row tables — it would have been easy to jump straight to `sec-hard-diligence` (it's labeled "THE CURRENT ... TABLE" right in the table listing) without confirming the date actually clears the 2026-01-01 boundary.

The three qualifiers (origin, value, goods) each have their own legend translating the plain-English question into a row code, and the legends are explicit that they are "the only place the mapping is written down" — guessing the code instead of reading the legend would risk picking the wrong row silently, since the row addresses (o2-value-w4-goods-k2 etc.) give no hint from the code alone which value band or goods category they represent.

The overlay-close step reported all five documents I read as "reached ... from somewhere the overlay never named" rather than "used" cleanly, because I read them directly via `table`/`read` instead of first adding them to the overlay with `overlay add`. The answer is correct regardless, but the intended workflow is to add each address to the working set with a reason as you go, not just read straight through — worth doing explicitly next time.
