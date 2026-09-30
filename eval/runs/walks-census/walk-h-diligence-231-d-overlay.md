1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W4, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods" --member /v1/nodes/hard-diligence-legend-revision/body "warning about three versions of diligence table, need to confirm which is current for today's date" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together"
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f8b89b --outcome answered --used /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**:
Yes, a site visit is required. The file (re-review) is looked at again every 6 months.
(Also on this row, though not asked: screening score required is 75, financial statements must be the last three years, audited.)

3. **Source**:
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body (the O3/W4/K2 row itself — site visit and re-review interval)
- /v1/nodes/hard-diligence-legend-revision/body (confirms this row's version, in force 2026-01-01 onwards, is the correct one for today, 2026-09-21)

4. **Notes**:
This one was more straightforward than expected — the procurement table listed the row address for origin O3/value W4/goods K2 directly (`hard-diligence-row-origin-o3-value-w4-goods-k2`), so no lookup of separate origin/value/goods legends was needed to translate a raw description into O3/W4/K2 codes; the question already gave the codes.
The one place I checked deliberately rather than assumed: the legend-revision page warns there are THREE versions of this table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onwards) and that reaching for the newest is wrong for older dates. Since the target row was under `sec-hard-diligence` (the current table, indexed by three qualifiers, per the legend), and today is 2026-09-21, the current version is correct — but this is exactly the kind of question where grabbing the first matching row without checking the date could silently give a superseded answer for a differently-dated question. Worth flagging: the overlay close marked the row I actually used as "reached" rather than "member," because I'd only added the parent table `sec-hard-diligence` as a member, not the specific row address — the overlay tool distinguishes between planned members and addresses actually read, which is a useful discipline but easy to trip on if you don't add the exact leaf address you end up citing.
