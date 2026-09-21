1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem

2. Answer
The overseas per-diem has been rewritten twice (three versions total, none formally withdrawn):
- Version 1, "Overseas allowance and exchange rate" — in force until 2024-07-01 (no stated start date; band-only, no grade or stay qualifier)
- Version 2, "Overseas per-diem, second version" — in force from 2024-07-01 to 2025-12-31 (adds grade as a qualifier)
- Version 3, "Overseas per-diem, current" — in force from 2026-01-01 onwards (adds stay length as a third qualifier)

3. Source
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/overseas-rates/body
/v1/nodes/hard-perdiem-v2/body
/v1/nodes/sec-hard-perdiem (table header)

4. Notes
The expense region table's own description line ("current table since 2026-01-01; the older band-only caps are still here and are superseded") reads as if there are only two versions — current vs. one older one. It would be easy to stop there and report "rewritten once." The dedicated legend file (hard-perdiem-legend-revision) is what surfaces that there are actually three versions, not two, and explicitly warns that the oldest version "says nothing at all about having been replaced" — so nothing in that oldest document itself would tip you off that it was superseded. The legend also warns that for a question dated in 2025 the correct table is the middle one (hard-perdiem-v2), not the oldest or the current — a trap that doesn't apply to this particular question (which asks for the whole history) but would matter for a dated lookup. The oldest version's address was not listed anywhere in the /v1/regions/expense table itself; I had to walk down through travel-expense → travel-overseas to find the actual printed address /v1/nodes/overseas-rates/body, which the legend file only referred to by short name ("overseas-rates").
