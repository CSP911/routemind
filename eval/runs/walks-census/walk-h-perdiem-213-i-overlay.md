1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Department head, Singapore, 3-week trip: hotel per night cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01, likely has hotel caps" --member /v1/nodes/evidence "what has to be attached for a spend to be accepted - receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_7c0de0 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body

2. **Answer**:
Lodging cap: 251 USD per night. Receipt required above: 44 USD.
(Department head = grade G3; Singapore = band B2; three weeks = stay S4, an exact match on the stay legend. This is the current overseas per-diem table, in force since 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → B2)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → S4)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body (lodging 251 USD/night, receipt threshold 44 USD)

4. **Notes**:
The expense table's warning that overseas per-diem has three superseded versions (hard-perdiem-legend-revision, hard-perdiem-v2, plus an older overseas-rates) made me deliberately pick the sec-hard-perdiem table (current, since 2026-01-01) rather than the superseded ones — worth flagging because it would be easy to grab a stale row by address-guessing.

The real near-miss was the receipt threshold. There is a second, unrelated "receipt threshold" concept in this domain: /v1/nodes/qualified-evidence → qualified-list/body, which sets a KRW-denominated ceiling (30,000 KRW) above which a simple receipt is not enough and qualifying evidence (tax invoice/invoice/card slip) is required for domestic expense claims generally. I opened it because the region table's evidence node looked like the obvious "receipt threshold" answer, and it would have been easy to report "30,000 KRW" as the answer to this question. But it's a different rule (currency, and general domestic evidence-quality gate, not an overseas per-diem lodging trip figure) and not what a department head planning a Singapore trip needs. The per-diem row itself already carries its own "Receipt threshold: 44 USD" field, which is the one that actually answers the question — no receipt needed for the daily allowance up to that per-day/incidentals amount, and above it evidence is required. I used the per-diem row's own field and discarded the KRW evidence table.

Stay length ("three weeks") mapped exactly to S4 ("three weeks") in the legend, so no rounding judgment was needed there — worth noting only because other legends (grade, band) required inexact "nearest entry" reasoning in general, though here department head and Singapore both matched exactly too.
