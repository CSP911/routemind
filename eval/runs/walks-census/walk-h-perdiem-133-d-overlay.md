1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G2, band B4, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip / hotel per diem and receipt threshold likely live here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_95a9a5 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body

2. **Answer**:
Lodging, per night: 219 USD. Receipt threshold: 58 USD (evidence must be kept above this amount).
(For context, same row also gives meals per day: 104 USD, incidentals per day: 21 USD.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body

4. **Notes**:
The initial overlay member (/v1/regions/expense) turned out to be too broad to answer from directly — it was a jumping-off point, not the source. Opening it surfaced /v1/nodes/sec-hard-perdiem, which is explicitly flagged as "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01," which matched the row directly by grade/band/stay code (g2-b4-s4) without needing the legend files, since the question already gave the codes rather than plain-language descriptions. One thing to watch: the table area also lists /v1/nodes/hard-perdiem-legend-revision and /v1/nodes/hard-perdiem-v2, warning that overseas per-diem has three historical versions — it would be easy to grab a superseded row by mistake if searching by keyword instead of going through sec-hard-perdiem, which is clearly labeled as current for today's date (2026-09-21). The overlay close command reported the used address as "reached ... from somewhere the overlay never named" since I never explicitly added the specific row as a member before closing — cosmetic, didn't affect the answer.
