1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/overseas-rates/body

2. **Answer**: USD 180 per night, for band B (China, South-East Asia, Eastern Europe).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (to determine which of the three per-diem versions is in force on 2024-06-29)
/v1/nodes/overseas-rates/body (the actual cap table)

4. **Notes**: The date given, 29 June 2024, is described as "two days before the first change" — the legend document confirms the first change to overseas per-diem happened on 2024-07-01, so 2024-06-29 falls just before it and is covered by the oldest version (`overseas-rates`, in force until 2024-07-01), not the "v2" table that starts on the change date. The legend document was essential here: it explicitly warns that the oldest version "says nothing at all about having been replaced," so without checking it first, reading `overseas-rates/body` alone would look self-contained and not raise any flag that a newer version exists — easy to mistake for the only/current answer even on a much later date. The near-miss risk was the opposite direction too: since the current table (`sec-hard-perdiem`) is billed as "the current table," it would be wrong to default to it for a 2024 date. Picking the middle version (`hard-perdiem-v2`) would also have been wrong here — that trap applies to 2025 dates, not this one, but the structure of the warning made it worth double-checking that 2024-06-29 isn't somehow inside the v2 window. It isn't: v2 starts 2024-07-01, one day after the question's date.
