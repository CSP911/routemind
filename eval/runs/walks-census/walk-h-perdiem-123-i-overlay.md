## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Team manager, Jakarta, 3 weeks - hotel per night cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table (since 2026-01-01) - by grade, band, stay length - should have hotel cap" --member /v1/nodes/hard-perdiem-legend-revision/body "warns which per-diem version applies to which dates - need to confirm current version applies" --member /v1/nodes/evidence "evidence table - likely holds receipt threshold rule" --member /v1/nodes/sec-trip-days-versus-allowance-days "trip days vs allowance days - 3 week trip may need this to compute stay length band"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d66e15 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body
```

## Answer

Lodging (hotel): **203 USD per night**.
Receipt required for any spend **over 49 USD** (the per-diem row's own "receipt threshold").

(For context, same row: meals 90 USD/day, incidentals 18 USD/day — not asked for but adjacent.)

This is grade G2 (team manager) × band B3 (Jakarta) × stay S4 (three weeks), from the current overseas per-diem table, in force since 2026-01-01.

## Source

- `/v1/nodes/hard-perdiem-legend-revision/body` — confirmed which of the three per-diem versions applies to today's date (2026-09-21 → current table, `sec-hard-perdiem`)
- `/v1/nodes/hard-perdiem-legend-grade/body` — team manager → grade G2
- `/v1/nodes/hard-perdiem-legend-band/body` — Jakarta → band B3
- `/v1/nodes/hard-perdiem-legend-stay/body` — three weeks → stay S4
- `/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body` — the row itself: 203 USD/night lodging, 49 USD receipt threshold

## Notes

- The per-diem area has three overlapping versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) covering different date ranges, and the revision-warning page is explicit that the oldest one "says nothing at all about having been replaced" — reaching for it directly (or trusting a stale bookmark) would silently give a wrong, superseded number. Checking that page first, before touching any figures, is what avoided that.
- Nearly missed that this table isn't looked up by destination/grade/duration names directly — it's indexed by three opaque qualifiers (grade, band, stay) that only the three legend pages translate. Skipping straight to guessing a row address (e.g. assuming "manager" = G1 or that "three weeks" rounds to S3 "eight nights") would have been wrong; the legend explicitly separates one-night/four-night/eight-night/three-week bands, and three weeks lands past the eight-night line into S4, not S3.
- There is a second, unrelated "receipt threshold" concept in `/v1/nodes/qualified-list/body` (general qualifying-evidence rules, ceiling of 30,000 KRW for a simple receipt vs. requiring a tax invoice/qualifying evidence). It looked like it might be the answer to "above what amount do I have to keep the receipt," but it's denominated in KRW for general domestic-style expense evidence, not the USD per-diem trip context asked about. The per-diem row itself already carries its own "Receipt threshold" field in USD (49 USD), which is the one that actually answers this question — the KRW evidence-ceiling table is a different rule for a different scope and would have been a wrong citation if used here.
