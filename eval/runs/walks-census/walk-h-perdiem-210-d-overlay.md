1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B2, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per night cap and receipt threshold for business trips are expense policy"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_569ba5 --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body

2. **Answer**: Lodging cap is 239 USD per night. The receipt threshold is 35 USD — above that amount, a receipt must be kept (this table is in force from 2026-01-01).

3. **Source**:
/v1/nodes/sec-hard-perdiem/body
/v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body

4. **Notes**: Straightforward once at the per-diem table — the grade/band/stay row addresses are literal (`hard-perdiem-row-grade-g3-band-b2-stay-s1`), so no legend lookup was needed since the question already gave codes rather than a job title, destination city, or trip length in days. The one thing worth flagging: the expense region's working set surfaced `hard-perdiem-legend-revision` and `hard-perdiem-v2`, warning that overseas per-diem has three superseded versions — it would be easy to grab the wrong version's figures if the codes matched a different table. Confirmed `sec-hard-perdiem` is "THE CURRENT... in force from 2026-01-01," which covers today's date (2026-09-21), so the v2/older figures were correctly avoided.
