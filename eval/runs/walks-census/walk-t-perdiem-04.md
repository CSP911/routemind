1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**: 115 USD nightly lodging cap (grade G2, band B2, under the version in force 2024-07-01 to 2025-12-31).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions covers October 2024)
- /v1/nodes/hard-perdiem-v2/body (the grade × band lodging cap table itself)

4. **Notes**: The expense table lists three per-diem-adjacent nodes (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), and its own row description flags that "the older band-only caps are still here and are superseded" — easy to mistake `sec-hard-perdiem` for authoritative since it's labeled "current" and "THE CURRENT OVERSEAS PER-DIEM TABLE" in caps. The legend document is explicit that reaching for the newest is wrong for pre-2026 dates, and that the oldest version (`overseas-rates`) never mentions being superseded, so nothing there would have warned me off it either. October 2024 falls cleanly in the 2024-07-01–2025-12-31 window, so `hard-perdiem-v2` is correct — but this is exactly the kind of date that's easy to get wrong by defaulting to the newest or oldest table instead of checking the legend first.
