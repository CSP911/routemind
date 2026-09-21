1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Team manager, Dhaka, one night: hotel per-diem cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade, destination band, and stay length" --member /v1/nodes/evidence "what has to be attached for a spend to be accepted - receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_9833a9 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body

2. **Answer**:
Lodging per night: 207 USD. Receipt is required above 49 USD (the per-diem row's own "Receipt threshold" field). This is from the current overseas per-diem table, in force from 2026-01-01, for grade G2 (team manager), band B4 (Dhaka), stay S1 (one night).

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body — maps "team manager" → grade G2
/v1/nodes/hard-perdiem-legend-band/body — maps "Dhaka" → band B4
/v1/nodes/hard-perdiem-legend-stay/body — maps "one night" → stay S1
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body — the row itself: lodging 207 USD/night, receipt threshold 49 USD

4. **Notes**:
The expense area's table lists a "receipt threshold" field right inside the per-diem row itself, which is the direct answer to "above what amount do I have to keep the receipt" in this context — no need to cross into the general evidence table. I did check /v1/nodes/qualified-evidence → /v1/nodes/qualified-list/body anyway, since "evidence" sounded like the natural place for a receipt-threshold question, but that table turns out to be a domestic, KRW-denominated rule (simple receipt fine up to 30,000 KRW, qualifying evidence required above it) — a different rule for a different currency/context, and using its 30,000 KRW figure here would have been wrong. The per-diem row's own USD-denominated "Receipt threshold: 49 USD" is the one that actually applies to an overseas hotel stay under this per-diem schedule. Also worth flagging: the expense region lists three versions of the overseas per-diem (a legend-revision doc, a superseded v2, and the current sec-hard-perdiem table) — picking the wrong one would silently give a stale rate, so I confirmed via the table listing that sec-hard-perdiem is the one "in force from 2026-01-01," which covers today's date (2026-09-21/20).
