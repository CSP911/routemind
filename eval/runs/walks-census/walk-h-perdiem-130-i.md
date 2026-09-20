## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body

## Answer
Lodging cap: 207 USD per night.
Receipt required above: 49 USD (the receipt threshold).

## Source
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date)
/v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
/v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
/v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body (the figures: lodging 207 USD/night, receipt threshold 49 USD)

## Notes
The expense region table flags up front that overseas per-diem has three superseded/current versions and warns that reaching for the newest is wrong for older dates — worth checking explicitly even though today's date (2026-09-20) turned out to need the current table (`sec-hard-perdiem`, in force since 2026-01-01) anyway. Skipping that check would have been a guess, not a verified answer.

The current per-diem table is indexed by three separate codes (grade, band, stay) each with its own legend file, none of which are guessable — "team manager" maps to G2, not G1, and Dhaka maps to B4 (the row order in the legend runs Tokyo/Singapore/Jakarta/Dhaka, cheapest-looking city last, which is easy to skim past if you assume band order follows some other logic). Requestor didn't state a grade explicitly but "team manager" is literally in the grade legend's left column, so no assumption was needed there.

The row itself has four figures (lodging, meals, receipt threshold, incidentals); only two were asked for (hotel cap and receipt threshold), so meals and incidentals were left out of the answer deliberately.
