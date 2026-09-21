1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "I have a claim dated in 2025 and I am not sure which version of the overtime rate applies to it. Where is that written down?" --member /v1/regions/payroll "overtime rate is a payroll figure; claim likely means overtime pay claim"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bff8da --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/payslip-overtime/body

2. **Answer**:
A 2025-dated claim uses the old (pre-2026-01-01) overtime rate table in payroll: +50% for overtime beyond the standard week, +50% for night work (10pm–6am), +50% for holiday work (first 8 hours), and +100% for holiday work beyond 8 hours — all applied to the hourly basic pay rate, and these premiums stack rather than replace one another. This old rule is explicitly correct only for dates before 2026-01-01, which covers the 2025 claim. From 2026-01-01 onward, the rate moved to attendance (`sec-hard-overtime`) instead — not applicable here since the claim is dated 2025.

3. **Source**:
/v1/nodes/hard-moved-overtime/body (establishes the 2026-01-01 cutover and confirms the old payroll page still governs anything before that date)
/v1/nodes/payslip-overtime/body (the actual pre-2026 overtime premium rates)

4. **Notes**:
The overlay's initial member list surfaced `/v1/nodes/hard-moved-overtime/body` directly, which was the key to answering correctly — without it I'd have just read `payslip-overtime` and stated the rates without flagging that they're version-gated to before 2026-01-01. That node made explicit that the page "was not withdrawn and nothing in them says they were replaced," which is exactly the kind of stale-looking-but-still-valid situation that could mislead a reader who didn't check for a newer version. Since the claim date (2025) falls before the cutover, the payroll-side rates are correct and the attendance-side `sec-hard-overtime` table (the post-2026-01-01 version) was correctly not needed. I did not visit the attendance region since the answer was already unambiguous from the payroll region's warning node, but if the claim date had been ambiguous or near the boundary, checking attendance would have been the next step.
