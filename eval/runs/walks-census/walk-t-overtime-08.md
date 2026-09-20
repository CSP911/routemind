1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body

2. **Answer**: For a 2025 claim, the payroll-page rates apply (they are correct for anything before 2026-01-01):
- Overtime (beyond the standard week): +50% of hourly basic pay
- Night work (10pm–6am): +50% of hourly basic pay
- Holiday work, first 8 hours: +50% of hourly basic pay
- Holiday work, beyond 8 hours: +100% of hourly basic pay
These premiums stack (add together) rather than replacing one another when more than one applies to the same hour.

3. **Source**:
- /v1/regions/payroll (pointed to the moved-overtime warning)
- /v1/nodes/hard-moved-overtime/body (established the 2026-01-01 cutoff and confirmed payslip-overtime is the correct old rule)
- /v1/nodes/payslip-overtime/body (the actual rate table)

4. **Notes**: The payroll region table itself flags, in its "when to be here" line, that overtime/night/holiday premium rates moved to attendance on 2026-01-01 and that the page still in payroll is the old rule — that's the tripwire that stops you from just grabbing whatever overtime table appears first. /v1/nodes/hard-moved-overtime/body spells out the cutoff explicitly and says the old page (payslip-overtime) "remains correct for anything dated before 2026-01-01 and for nothing after it," which is exactly what makes the 2025 claim date decisive. Since the claim predates the cutoff, I never opened attendance's sec-hard-overtime — but if the claim date had been ambiguous or straddled the boundary, that would have been the wrong call to skip. The only mildly confusing step was that payslip-overtime isn't listed directly under /v1/nodes/payslip; you have to go one level deeper into sec-payslip-lines-in-detail to find it, even though the hard-moved-overtime warning already gives its exact address, so that detour wasn't strictly necessary for the answer, only for confirming the address existed where expected.
