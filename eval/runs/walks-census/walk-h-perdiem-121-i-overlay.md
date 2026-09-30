1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Team manager, Jakarta, 4 nights: hotel per-diem cap per night and receipt threshold above which receipt must be kept?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force 2026-01-01" --member /v1/nodes/evidence "receipt requirement threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-evidence/body
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e1c2ae --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body

2. **Answer**:
Lodging cap: 195 USD per night. Receipt threshold: 43 USD — above this amount a receipt must be kept (this is the current overseas per-diem table, in force since 2026-01-01, for grade G2 / band B3 / stay S2).

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
/v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
/v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body (lodging 195 USD/night, receipt threshold 43 USD)

4. **Notes**:
"What can I put on a hotel each night" and "above what amount do I have to keep the receipt" are both answered by the same single per-diem row once grade/band/stay are resolved through the three legend tables — no need to combine documents beyond that.

The one place I nearly went wrong: the expense table also lists /v1/nodes/qualified-evidence (and its child /v1/nodes/qualified-list), which gives a general receipt-evidence rule — but in KRW (30,000 KRW simple-receipt ceiling) for domestic-style evidence handling, unrelated to this overseas per-diem's own USD receipt threshold. I read both to check whether they applied here and rejected them: they answer a different question (what counts as qualifying evidence for tax purposes generally) in a different currency, not the overseas per-diem receipt threshold this question asked about. Using the KRW figure here would have been a currency-context mismatch. The per-diem row itself already carries its own "Receipt threshold" field, which is the correct, self-contained answer.

Also worth flagging: the expense table's own description warns overseas per-diem has three superseded/current versions (hard-perdiem-legend-revision, hard-perdiem-v2, sec-hard-perdiem/current). I picked /v1/nodes/sec-hard-perdiem as it's explicitly labeled the table in force from 2026-01-01, and today is 2026-09-21, so it's current — didn't need to open the superseded versions, but the naming makes it easy to grab the wrong one if not read carefully.
