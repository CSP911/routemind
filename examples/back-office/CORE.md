# Core

The back-office of one fictional company. The amounts and deadlines written here are that company's
own policy, not the law itself. Where the law does set something — retention periods, tax-free caps,
insurance rates — the authority is named alongside it.

Office work asks two kinds of question all day: **"am I allowed to do this"** and **"who do I give
what to, and by when"**. So the areas are cut by **where a question is headed**, not by which team
owns it. One business trip splits three ways: how many days count is ATTENDANCE, how much is paid is
EXPENSE, whether it is taxed is PAYROLL.

## What hangs on what

**Anything that spends money is decided by the amount first.** Purchase or expense, the amount band
sets the approval chain (PROCUREMENT's threshold table), and that band comes from APPROVAL's
delegation rules. So "how far up does this go" starts in purchasing and ends in approval. Splitting a
payment to land in a lower band is refused in every area.

**A spend survives on its evidence.** EXPENSE's qualifying-evidence rule governs, and 30,000 KRW is
the boundary. Anything paid by card is fine even when the paper receipt is lost, because the card slip
is itself qualifying evidence — the trouble is always cash.

**A trip passes through three areas in order.** Attendance confirmed (ATTENDANCE) → allowance and
expenses settled (EXPENSE) → taxed or not (PAYROLL). Out of order it comes back: a day with no
attendance pays no allowance, and an allowance paid anyway is not tax free. The node that joins those
three points is "Handover from trip to settlement".

**Some deadlines are ours and some are not.** Attendance closing on the 3rd and purchase requests
closing Tuesday and Thursday are internal, so there is room to move. The year-end cut-off of 31
January and the retention periods are tied to filing calendars and statute, and do not move. For those
the answer is a different route — the May tax return, an amended claim.

**Some questions only end with a person.** Attendance the rules do not cover is the HR desk; amounts
and suppliers are the office & purchasing desk; templates, seals and destruction are the records desk;
pay, insurance and settlement are the payroll desk. Each area carries its desk as a node, so a question
the written rule does not answer ends there rather than nowhere.

## Areas

| Area | What it holds |
|---|---|
| `ATTENDANCE` | Leave, parental leave, and what counts as time worked |
| `EXPENSE` | Card and travel spending, and what counts as evidence |
| `PROCUREMENT` | Purchase requests, vendor selection, contracts and their custody |
| `APPROVAL` | Drafting, approval chains, delegated authority and document retention |
| `PAYROLL` | Pay and deductions, social insurance, and the year-end tax settlement |
