1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/leave-accrual/body
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body

2. **Answer**: 15 days. Two years of continuous service falls in the "1 year and over" tier (15 days, granted whole on 1 January); the "3 years and over" tier (15 + 1 per two further years) does not yet apply.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/leave-accrual/body
/v1/nodes/accrual-rule/body
(/v1/nodes/hard-accrual-v2/body used only to confirm the 2024-07-01 cutover date and that the pre-cutover rule is the one in leave-accrual)

4. **Notes**: The date arithmetic is the whole trick here — "the first change" is the 2024-07-01 cutover named in hard-accrual-legend-revision and confirmed again in hard-accrual-v2/body ("Before 2024-07-01 the rule was the one in leave-accrual"). 29 June 2024 is two days before that, so the applicable rule is the OLDEST version (indexed by service length alone, at /v1/nodes/leave-accrual), not the two-qualifier hard-accrual-v2 table that only starts on 2024-07-01. It would have been easy to grab hard-accrual-v2 by reflex since it's the one literally addressed to "2024" in its title-adjacent text, but its own body explicitly disclaims responsibility for anything before 2024-07-01. The legend page's own worked example ("For a question dated in 2025 the answer is the middle one") is a red herring for this specific date — it's warning about 2025, not 2024-06-29, so I didn't let it steer me toward hard-accrual-v2. No document was found literally dated "29 June 2024"; the phrase in the question describes the target date for applying the rule, not a document with that date stamp — I confirmed this by checking the region table and leave-accrual table and finding no such dated memo.
