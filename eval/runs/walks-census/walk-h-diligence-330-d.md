1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body

2. Answer:
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row, for context: screening score required 90; financial statements — last three years, audited.)

3. Source:
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body

4. Notes:
The origin/value/goods codes (O4, W4, K1) were already given in coded form in the question, so no
detour into the legend files (hard-diligence-legend-origin/value/goods) was needed to translate raw
descriptions into codes — that shortcut could easily be missed on a differently-phrased question.
The procurement table surfaced a loud warning row (`hard-diligence-legend-revision`, "supplier due
diligence has THREE versions") plus a superseded `hard-diligence-v2` table right next to the current
one — easy to grab the wrong version by accident. The current table (`sec-hard-diligence`) states
plainly it is "in force from 2026-01-01," which covers today's date (2026-09-20), so it's correct
without needing to open the revision-legend file. No ambiguity once the right table was found; the
main risk was stopping at the superseded `hard-diligence-v2` table instead of `sec-hard-diligence`.
