---
name: daily-brief
description: The morning read on Todd's Appraisal Tracker — what is overdue, what is due this week, what still needs an inspection date, what is sitting in the tracker wrong, and what has been delivered but never marked paid. Read-only off the newest tracker auto-backup; it never writes to the tracker. Use when Todd asks for his brief, his day, his week, what is on his plate, what is due, what is late, or where the pipeline stands. Triggers on "daily brief", "morning brief", "what's on my plate", "what's due", "what's late", "where do I stand", "run the brief".
---

# Daily brief — the morning read on the tracker

```bash
python3 ~/.claude/skills/daily-brief/daily_brief.py            # print it
python3 ~/.claude/skills/daily-brief/daily_brief.py --days 10  # wider due window
python3 ~/.claude/skills/daily-brief/daily_brief.py --date 2026-09-20   # pretend
```

Reads the **newest** `appraisal-tracker-auto-*.json` in
`C:\Users\toddp\OneDrive\Appraisal Tracker\Appraisal Tracker - Backups`.

**It is read-only, and it must stay that way.** The tracker's live data is
`localStorage` in the browser on the Pinewood desktop; this only ever sees the
backup. The app's one import path is Restore, which *replaces every file* — never
use it to apply a single change. Writing back is a separate, unbuilt piece; see
the parked design in memory before starting it.

## What it reports, in order

1. **Overdue** — open files past their due date. Only appears when there are some.
2. **Due in the next N days** — with the client, the product, and a flag when no
   inspection date is on file.
3. **Inspections** — what is actually on the calendar, then the files marked
   Inspected that carry no date. That date is the effective date, so it is the
   one piece of missing data that changes conclusions rather than just tidiness.
4. **Needs a fix in the tracker** — one line per file, not one per problem:
   missing public-record pull (only flagged once the file is due inside the
   window, since before that it is just work not yet done), no order sheet
   attached, contract price not parsed.
5. **Look at these** — an order with a real order number and fee but no due date
   and no county, usually because the order parser took the client's own office
   address as the subject. These are the ones that sit for weeks unnoticed.
6. **Delivered, not marked paid** — last, and captioned, because it is only
   meaningful if he keeps the Paid status current.

Statuses in the real data are `New`, `Inspected`, `Delivered`, `Paid`,
`Cancelled`. Open means not Delivered, Paid, or Cancelled.

## Sending it

Both delivery flags take the body on stdin and are wired already:

```bash
python3 ~/.claude/skills/daily-brief/daily_brief.py --email   # to mpenny.ai@gmail.com
python3 ~/.claude/skills/daily-brief/daily_brief.py --note    # to Notion Quick Notes
```

**Show him the brief and get a go-ahead before using either flag.** Both are
outward-facing, and the email skill's confirmation rule applies here too. Running
it with no flag and pasting the output into the conversation needs no permission —
that is the normal path when he asks for it in a session.

## Scheduling it

It has to run where OneDrive is, so the laptop or Pinewood — a cloud schedule
cannot see the backup folder. Nothing is scheduled right now; it runs when asked.
If he wants it automatic, the options are a WSL cron entry on the laptop or a
Windows Task Scheduler job on Pinewood, and either one needs that machine awake at
the time it fires. Ask which machine before setting anything up.

## Reading it back to him

Lead with the one thing that actually needs a decision today, not with the section
order. If nothing is overdue, say so in the first sentence — he is checking this to
find out whether he can stop thinking about it.
