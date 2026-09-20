1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body

2. Answer

For grade G3, band B4, stay S4 (in force from 2026-01-01):
- Lodging (hotel), per night: 283 USD
- Receipt required above: 62 USD (receipt threshold)

3. Source

/v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body

4. Notes

The route was direct — /v1/regions/expense listed /v1/nodes/sec-hard-perdiem as "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01," and its table listed a row for exactly G3/B4/S4, so no legend lookups for grade/band/stay codes were needed since they were given pre-coded in the question. The one thing worth flagging: the expense region also lists /v1/nodes/hard-perdiem-legend-revision/body and /v1/nodes/hard-perdiem-v2/body, both older/superseded versions of the per-diem table, sitting right next to the current one with very similar names. It would be easy to grab the wrong version if you didn't read the "WARNING — THREE versions" note and the "current since 2026-01-01" framing carefully. I did not open the superseded versions since the row I read already stated its own effective date range (2026-01-01 onward) and today's date falls within it, confirming it's current — but the naming similarity is a real trap in this table.
