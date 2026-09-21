1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "G2/B3/S2: hotel per night amount, receipt threshold" --member /v1/regions/expense "expense region covers business trip pay and receipts"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_494e41 --outcome answered --used /v1/regions/expense /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body

2. **Answer**: Lodging (hotel), per night: 195 USD. Receipt threshold: 43 USD (evidence is required above this amount).

3. **Source**:
- /v1/nodes/sec-hard-perdiem (table listing the per-diem rows)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body (the row itself, figures used)

4. **Notes**: The expense region's working set surfaced two overseas per-diem documents besides the current table: `hard-perdiem-legend-revision` (a warning that three versions exist) and `hard-perdiem-v2` (explicitly marked superseded, in force 2024-07-01 to 2025-12-31). I did not need to open either — the current table (`sec-hard-perdiem`) states plainly it is "in force from 2026-01-01" and today is 2026-09-21, so it's current, and the row itself repeats that same in-force date and names the prior versions for contrast. Still, a walker moving faster than I did could easily grab `hard-perdiem-v2`'s numbers by mistake since it sits right next to the current table in the listing with a very similar name — worth flagging as the one place this walk could have gone wrong.
