1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D2, hours H2, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision/body "warns overtime rate has three versions with different date ranges - need to confirm which applies"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e83dda --outcome answered --used /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body /v1/nodes/hard-overtime-legend-revision/body

2. **Answer**:
Multiplier: 1.83x. Rounding: to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body
/v1/nodes/hard-overtime-legend-revision/body

4. **Notes**:
The question gave no date, so the answer depends on assuming "today" (2026-09-21) is the governing date. The legend-revision page is explicit that this subject has three versions and "the oldest says nothing at all about having been replaced" — reaching straight for the newest table without checking would have been an unverified assumption, not a mistake avoided by luck. Since no date was named in the question, I treated it as a present-tense question and confirmed against the revision legend that 2026-01-01 onwards (the `sec-hard-overtime` table, indexed by three qualifiers: day, hours, place) is the one in force now, which matches the three qualifiers (D2, H2, P2) given in the question. Had the question specified a 2025 date, the correct source would have been `hard-overtime-v2` instead. The row address itself was never printed until I created the overlay under the parent table — I did not construct it, only used the address the overlay table printed.
