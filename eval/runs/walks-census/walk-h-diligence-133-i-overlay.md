1. Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 700,000,000, licensed vendor: on-site premises visit required? review/renewal frequency for the file?" --member /v1/regions/procurement "amount+category threshold table, vendor onboarding due diligence likely lives here"
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_fc4a4f --outcome answered --used /v1/nodes/hard-diligence-legend-origin /v1/nodes/hard-diligence-legend-value /v1/nodes/hard-diligence-legend-goods /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4

2. Answer

Yes, a site visit is required. The file is re-reviewed every 6 months.

(Row derived from the legends: Stuttgart → origin O2, seven hundred million won → value W4, a licence → goods K4. This row is in force from 2026-01-01, current as of today 2026-09-21.)

3. Source

/v1/nodes/hard-diligence-legend-origin/body (Stuttgart → O2)
/v1/nodes/hard-diligence-legend-value/body (seven hundred million won → W4)
/v1/nodes/hard-diligence-legend-goods/body (a licence → K4)
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body (Site visit: yes; Re-review interval: every 6 months)

4. Notes

The procurement table surfaced two similarly-named due-diligence tracks: a legacy "where to start" overview (sec-supplier-due-diligence, with four narrative sub-pages on sanctions/code of conduct/disqualification) and the actual lookup table (sec-hard-diligence) indexed by origin/value/goods codes. The narrative overview never mentions site visits or a review cadence at all — those numbers only live in the individual origin/value/goods row. It would be easy to read the overview, conclude "checks exist but no premises visit is specified," and stop there without ever reaching the row that actually has the numbers.

There's also a live trap: the table's own listing (sec-hard-diligence) is flagged "THE CURRENT ... in force from 2026-01-01," and a sibling node hard-diligence-legend-revision warns there are three versions of this table with different rules. I did not open that revision-warning file, but the row I read self-declares its effective range (2026-01-01 onward, with older versions named as hard-diligence-v2 and supplier-due-diligence) and today's date, 2026-09-21, falls inside it, so I'm confident this is the correct version without needing to open the warning file separately.

The three legend tables (origin/value/goods) are the only place the O2/W4/K4 codes are decoded — the question's plain-language terms ("a firm in Stuttgart," "seven hundred million won," "a licence") map to codes only through those tables, and the 64-row matrix gives no other way in.
