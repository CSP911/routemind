1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "MD, Tokyo, 3 weeks: hotel per night cap and receipt threshold?" --member /v1/regions/expense "business trip lodging amounts and receipt rules live here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_90ab46 --outcome answered --used /v1/regions/expense /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s4/body

2. **Answer**: Lodging cap is 299 USD per night. Receipt is required above 39 USD (the receipt threshold).

3. **Source**:
/v1/regions/expense
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/sec-hard-perdiem
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s4/body

4. **Notes**: This subject has three superseded versions of the per-diem table (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the warning page is explicit that grabbing the newest one is only correct for dates from 2026-01-01 onward — today (2026-09-21) qualifies, but it would have been easy to skip that check and just grab whichever table looked most current without confirming the date band. The row itself is selected by three independent legends (grade, band, stay) that must each be resolved separately before the row address can be built — "managing director" isn't a literal match anywhere in the row table, it only resolves through the grade legend to G4, same for Tokyo→B1 and "three weeks"→S4. Nothing here was ambiguous once the legends were read; the main risk was assuming rather than verifying the date-validity of the table version.
