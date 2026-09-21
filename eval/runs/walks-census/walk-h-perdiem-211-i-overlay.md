1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Department head, Singapore, four nights — hotel cap per night, and receipt threshold" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel caps" --member /v1/nodes/evidence "what has to be attached for a spend to be accepted — likely receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-evidence/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6d41fd --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body

2. Answer

Lodging cap: 243 USD per night. Receipt required above: 38 USD (per-diem receipt threshold for this row). This is from the current overseas per-diem table (in force since 2026-01-01), row grade G3 (department head) × band B2 (Singapore) × stay S2 (four nights).

3. Source

/v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
/v1/nodes/hard-perdiem-legend-band/body (Singapore → B2)
/v1/nodes/hard-perdiem-legend-stay/body (four nights → S2)
/v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body (243 USD lodging/night, 38 USD receipt threshold)

4. Notes

The expense table warns up front that overseas per-diem has three superseded/current versions (hard-perdiem-legend-revision, hard-perdiem-v2, sec-hard-perdiem). I went straight for sec-hard-perdiem, the one flagged as current since 2026-01-01, and the row itself restates "In force from 2026-01-01" — today is 2026-09-21, so no version check needed beyond that self-declaration.

The near-miss: the expense area also has a "qualified-evidence" table with its own receipt threshold ("up to 30,000 KRW a simple receipt is accepted"). That's a different, domestic/KRW rule about which document type qualifies as evidence, unrelated to this USD overseas per-diem claim — easy to grab as "the" receipt threshold if you don't read past the number. The per-diem row already carries its own "Receipt threshold: 38 USD" field, which is the one that actually answers the question for this trip; I checked qualified-evidence to rule it out rather than to use it.

Also worth flagging: the per-diem row's grade/band/stay legends explicitly say to take the nearest entry above if your case isn't listed exactly — didn't need that fallback here since department head, Singapore, and four nights are all exact matches in their respective legends, but it's a trap for a walk where the inputs don't land on a listed row.
