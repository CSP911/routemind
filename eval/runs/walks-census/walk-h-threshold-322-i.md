1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m3/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**
"Dinner with a client" = category C4, "around 12 million won" = amount V3, "locked in for three years" = term M3 (delegation limit 20,058 thousand KRW). The division director signs it off, and three competing quotes are required. Expect 10 working days.

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m3/body
/v1/nodes/hard-threshold-legend-revision/body (confirms table validity for 2026-09-21)

4. **Notes**
The scenario's wording lines up almost verbatim with the three legend tables' example rows ("dinner with a client", "around 12 million won", "locked in for three years"), which made row selection unambiguous once the legends were read — but it would have been easy to skip the legends and guess a category/amount/term code directly, which the instructions explicitly warn against. The bigger risk was the version trap: procurement's approval threshold has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the table listing initially shows both the current and a superseded (`hard-threshold-v2`) row side by side with similar names — grabbing the wrong one without checking the revision legend against today's date (2026-09-21) would have silently produced a stale answer. Also worth flagging: "locked in for three years" read at first like a contract-only concept unrelated to a one-off dinner, which could tempt skipping straight to the expense region instead of procurement; the category legend confirms client dinners are handled under procurement's threshold table regardless of how casual the event sounds.
