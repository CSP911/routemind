1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Which version of the overseas per-diem applies to a claim dated in 2025?" --member /v1/regions/expense "business trip pay / overseas per-diem rates are covered under expense"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_021c1b --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-v2/body

2. **Answer**:
Overseas per-diem has three versions, indexed by date in force:
- until 2024-07-01: `overseas-rates` (one qualifier)
- 2024-07-01 to 2025-12-31: `hard-perdiem-v2` (two qualifiers: grade and band)
- 2026-01-01 onwards: `sec-hard-perdiem` (current, three qualifiers: grade, band, stay)

A claim dated anywhere in 2025 falls in the middle range (2024-07-01 to 2025-12-31), so the applicable version is `hard-perdiem-v2`: the nightly lodging cap table by grade (G1–G4) and band (B1–B4), e.g. G1/B1 = 95 USD up to G4/B4 = 155 USD. The daily meal allowance and receipt threshold for that period followed the older `overseas-rates` rule unchanged, since those figures were not revised in this version.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body — the routing page that says which date maps to which version
/v1/nodes/hard-perdiem-v2/body — the actual 2024-07-01 to 2025-12-31 figures

4. **Notes**:
The expense table's per-diem entries are easy to misread at a glance: `sec-hard-perdiem` is labeled "THE CURRENT OVERSEAS PER-DIEM TABLE" and sits right there, tempting a reader to grab it for any per-diem question without checking the date. The legend/revision page exists specifically to head that off — it says outright that reaching for the newest is wrong for anything before 2026-01-01, and that the oldest version (`overseas-rates`) says nothing about being superseded, so nothing there would flag itself as wrong either. Since the claim is dated in 2025, the correct answer is the middle version, not the current one — the kind of claim it would have been easy to get wrong without opening the legend page first.
