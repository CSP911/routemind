---
id: overtime-system-entry
name: "Where overtime is recorded"
kind: system
one_liner: "The groupware menu that holds overtime requests, separate from the leave and trip menus"
parent: sec-overtime-and-hours
---
# Where overtime is recorded

Overtime requests are filed in the groupware's Overtime menu, not the Leave or Trip menus used elsewhere in attendance. Each entry carries the requested start and end time, the manager's approval status, and — once worked — the actual hours logged against it.

## What lives here
- The original request and its approval, timestamped before the overtime starts.
- Any late filing within the 3-working-day exception window, with the reason recorded.
- The night/holiday flags that trigger the relevant premium, set automatically from the time window.

**The Overtime menu does not pull from the ordinary clock-in/clock-out record automatically — a request has to be entered separately even if the extra hours are already visible in the attendance log.** That gap is exactly how hours end up worked and never requested: the system shows the hours were there, but shows no request against them.

The general attendance menus are covered separately for where leave and trip records live.
