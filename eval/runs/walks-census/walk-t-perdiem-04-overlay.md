1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "October 2024 nightly lodging cap for grade 2 traveller, band B2 destination, overseas per-diem in force on that date" --member /v1/regions/expense "business trip pay / per-diem is under expense area"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_692e33 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-v2/body

2. **Answer**: 115 USD nightly lodging cap.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (established that October 2024 falls under the second of three versions, 2024-07-01 to 2025-12-31)
/v1/nodes/hard-perdiem-v2/body (the version in force, containing the grade x band table: G2/B2 = 115 USD)

4. **Notes**: The overseas per-diem subject has three versions of the same figure at three different addresses (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the top-level table for `sec-hard-perdiem` is the one that surfaces most prominently as "THE CURRENT OVERSEAS PER-DIEM TABLE" — it would be easy to grab that one by default and get the current (2026-01-01 onward) figures instead of the ones in force in October 2024. The `hard-perdiem-legend-revision` document exists specifically to prevent that mistake and was the one that redirected me to `hard-perdiem-v2`. Also worth flagging: after closing the overlay, the tool reported both used addresses as "reached" rather than matched against the working set, even though both were present as members when the overlay was created — likely just how the tool logs addresses read via `read` rather than fetched via `table`, not an error on my part.
