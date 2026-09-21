1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Tokyo one night hotel cap for a team manager, and receipt threshold" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/destination band/stay, likely has hotel caps" --member /v1/nodes/evidence "receipt threshold for evidence of spend"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_d94bca --address /v1/nodes/qualified-evidence --why "domestic KRW receipt-qualification threshold, not the overseas per-diem receipt threshold asked about"
./bench/rmcli.py overlay close --id ov_2026-09-21_d94bca --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body

2. **Answer**: For a team manager (grade G2) staying one night (stay S1) in Tokyo (band B1), current overseas per-diem table (in force from 2026-01-01): lodging cap is 159 USD per night. The receipt threshold on this same row is 22 USD — above that amount, the receipt must be kept.

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body

4. **Notes**: The expense area's table listing warns up front that overseas per-diem has three versions in force over different date ranges (hard-perdiem-legend-revision, hard-perdiem-v2, and the current sec-hard-perdiem since 2026-01-01) — easy to grab the wrong one if you don't check the "in force from" line. I confirmed the row I read states "In force from 2026-01-01," which covers today (2026-09-21), so it's the right version. The three "qualifiers" (grade, band, stay) each have their own legend file that must be read first — the row addresses themselves give no hint which grade a "team manager" or which band "Tokyo" maps to; you have to decode via the legends (team manager → G2, Tokyo → B1, one night → S1) before the row address can even be built from the table listing. I also nearly conflated the per-diem row's own "Receipt threshold" field (22 USD, specific to this grade/band/stay combination) with the separate, general "Qualifying evidence" table (/v1/nodes/qualified-evidence → qualified-list), which gives a 30,000 KRW threshold for when a simple receipt is no longer sufficient. That KRW table is about domestic expense-evidence *type* (tax invoice vs. simple receipt) in a different currency and is not the per-diem row's receipt threshold — I checked it, confirmed it was a different, unrelated figure, and excluded it from the answer.
