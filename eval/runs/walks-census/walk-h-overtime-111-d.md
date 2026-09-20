1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body

2. **Answer**:
Multiplier: 1.83x. Minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body

4. **Notes**:
The top-level table lists five areas and none is named "overtime" — the natural first guess is payroll, since overtime pay sounds like a payslip line. Opening /v1/regions/payroll confirms that guess is wrong: it explicitly warns that overtime, night and holiday premium rates moved to attendance on 2026-01-01, and the payroll page is "the old rule." That warning is the only thing that kept me from reading the superseded payroll-side overtime figures.

Inside attendance there are two competing overtime nodes: `hard-overtime-v2` (marked SUPERSEDED, in force 2024-07-01 to 2025-12-31) and `sec-hard-overtime` (marked "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01"). Today's date (2026-09-20) falls under the current table, so `sec-hard-overtime` is the right one — but it would be easy to grab the wrong version if not reading the "in force" dates carefully, since both are named similarly ("hard-overtime...").

The question already gave day/hours/place as codes (D2, H2, P2) rather than plain-English descriptions, so no legend lookup (day/hours/place legend files) was needed to translate a real-world scenario into codes — the row address was constructable directly from the codes given. Had the question instead described an actual day, hour count, and location in prose, the three legend files under `sec-hard-overtime` (day, hours, place) would have been required first.
