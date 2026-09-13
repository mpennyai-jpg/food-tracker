#!/usr/bin/env python3
"""
daily_brief.py — the morning read on the Appraisal Tracker.

Read-only. Takes the newest Appraisal Tracker auto-backup and answers, in one
screen on a phone: what is late, what is due, what has to be inspected, what is
sitting in the tracker wrong, and what has been delivered but never marked paid.

Writes nothing to the tracker and never touches the live data.

  python3 daily_brief.py                    # print it
  python3 daily_brief.py --days 10          # widen the due window
  python3 daily_brief.py --email            # mail it to himself
  python3 daily_brief.py --note             # push it to Notion Quick Notes
"""
import argparse, datetime as dt, glob, json, os, subprocess, sys

BACKUPS = "/mnt/c/Users/toddp/OneDrive/Appraisal Tracker/Appraisal Tracker - Backups"
EMAIL_TOOL = os.path.expanduser("~/.claude/skills/email/email_tool.py")
NOTE_TOOL = os.path.expanduser("~/.claude/skills/send-note/send_note.py")

CLOSED = {"delivered", "paid", "cancelled"}   # no longer needs work
DONE = {"paid", "cancelled"}                  # off the books entirely
W = 62


def newest_backup(d=BACKUPS):
    fs = sorted(glob.glob(os.path.join(d, "appraisal-tracker-auto-*.json")),
                key=os.path.getmtime)
    if not fs:
        sys.exit(f"no auto-backup found in {d}")
    return fs[-1]


def d(v):
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except (TypeError, ValueError):
        return None


def human(day, today):
    n = (day - today).days
    if n == 0: return "TODAY"
    if n == 1: return "tomorrow"
    if n == -1: return "1 day late"
    if n < 0: return f"{-n} days late"
    return f"{n} days"


def addr(r):
    a = " ".join(((r.get("address") or "?").strip().rstrip(" ,")).split())
    c = (r.get("city") or "").strip().title()
    return f"{a}, {c}" if c else a


def rule(ch="-"):
    return ch * W


def short(r):
    """Street address alone — for packing several onto one line."""
    return " ".join(((r.get("address") or "?").strip().rstrip(" ,")).split())


def build(recs, today, days):
    open_files = [r for r in recs if (r.get("status") or "").lower() not in CLOSED]
    L = []

    # ---- bucket the open files
    overdue, due_soon, undated = [], [], []
    for r in open_files:
        dd = d(r.get("dueDate"))
        if dd is None:
            undated.append(r)
        elif dd < today:
            overdue.append((dd, r))
        elif (dd - today).days <= days:
            due_soon.append((dd, r))
    overdue.sort(key=lambda x: x[0])
    due_soon.sort(key=lambda x: x[0])

    head = [f"{len(open_files)} open"]
    if overdue:
        head.append(f"{len(overdue)} OVERDUE")
    head.append(f"{len(due_soon)} due in {days}d")
    L.append(f"PINEWOOD - {today:%A, %B %-d, %Y}")
    L.append(" | ".join(head))
    L.append(rule("="))

    def line(dd, r, flag_undated=True):
        L.append(f"  {dd:%a %m/%d}  {human(dd, today):<11} {addr(r)}")
        tail = " · ".join(x for x in [r.get("status"), r.get("product"),
                                      r.get("amc") or r.get("lender")] if x)
        L.append(f"              {tail}")
        if flag_undated and not d(r.get("inspectionDate")):
            L.append("              >> no inspection date")

    if overdue:
        L.append("")
        L.append(f"** OVERDUE ({len(overdue)}) **")
        for dd, r in overdue:
            line(dd, r)

    L.append("")
    L.append(f"DUE IN THE NEXT {days} DAYS ({len(due_soon)})")
    if not due_soon:
        L.append("  Nothing.")
    for dd, r in due_soon:
        line(dd, r)

    # ---- inspections: the calendar, then the missing dates, once
    sched = sorted(((d(r.get("inspectionDate")), r) for r in open_files
                    if d(r.get("inspectionDate"))), key=lambda x: x[0])
    upcoming = [(x, r) for x, r in sched if x >= today]
    noins = [r for r in open_files if not d(r.get("inspectionDate"))
             and (r.get("status") or "").lower() == "inspected"]

    L.append("")
    L.append("INSPECTIONS")
    if upcoming:
        for x, r in upcoming[:8]:
            t = (r.get("inspectionTime") or "").strip()
            L.append(f"  {x:%a %m/%d}  {t:<9} {addr(r)}")
    else:
        L.append("  Nothing on the calendar.")
    if noins:
        L.append("")
        L.append(f"  {len(noins)} marked Inspected with no date. That date is the")
        L.append("  effective date, so it has to be right before the report goes:")
        for r in noins:
            dd = d(r.get("dueDate"))
            L.append(f"    {short(r)}" + (f"  (due {dd:%m/%d})" if dd else ""))

    # an order with no subject address belongs in its own block, not the fix list
    orphans = [r for r in open_files
               if not d(r.get("dueDate")) and not (r.get("county") or "").strip()]
    orphan_ids = {id(r) for r in orphans}

    # ---- one line per file that needs something, not one per issue
    probs = {}
    for r in open_files:
        if id(r) in orphan_ids:
            continue
        why = []
        dd = d(r.get("dueDate"))
        soon = dd is not None and (dd - today).days <= days
        if not (r.get("address") or "").strip() or not dd:
            why.append("no due date" if not dd else "no address")
        if soon and not (isinstance(r.get("pub"), dict) and r["pub"]):
            why.append("no public-record pull")
        if not (r.get("attachments") or []):
            why.append("no order sheet attached")
        con = r.get("contract") or {}
        if con and not str(con.get("price") or "").strip():
            why.append("contract price not parsed")
        if why:
            probs[short(r)] = why
    if probs:
        L.append("")
        L.append(f"NEEDS A FIX IN THE TRACKER ({len(probs)})")
        for k, why in probs.items():
            L.append(f"  {k} - {', '.join(why)}")

    # ---- an order with no subject address is the one that gets forgotten
    if orphans:
        L.append("")
        L.append("LOOK AT THESE - order on file, subject details missing")
        for r in orphans:
            od = d(r.get("orderDate"))
            age = f", sitting {(today - od).days} days" if od else ""
            L.append(f"  {r.get('lender') or r.get('amc') or 'client ?'} "
                     f"#{r.get('orderNo') or '?'}{age}")
            L.append(f"    address reads: {short(r)}, "
                     f"{(r.get('city') or '').title()} {r.get('statezip') or ''}".rstrip())
            L.append("    -- that looks like the client's own office, not the subject.")

    # ---- money, last, because it is the least urgent
    unpaid = [r for r in recs if (r.get("status") or "").lower() == "delivered"]
    if unpaid:
        unpaid.sort(key=lambda r: d(r.get("dueDate")) or dt.date(1900, 1, 1))
        tot = 0.0
        for r in unpaid:
            try:
                tot += float(str(r.get("fee") or 0).replace("$", "").replace(",", ""))
            except ValueError:
                pass
        L.append("")
        L.append(f"DELIVERED, NOT MARKED PAID ({len(unpaid)}"
                 + (f" | ${tot:,.0f}" if tot else "") + ")")
        for r in unpaid[:4]:
            dd = d(r.get("dueDate"))
            when = f"{dd:%m/%d}" if dd else "  ?  "
            L.append(f"  {when}  {addr(r)} - {r.get('amc') or r.get('lender') or '?'}")
        if len(unpaid) > 4:
            L.append(f"  ... and {len(unpaid) - 4} more")
        L.append("  (Only worth reading if you keep the Paid status current.)")

    counts = {}
    for r in recs:
        counts[r.get("status") or "(blank)"] = counts.get(r.get("status") or "(blank)", 0) + 1
    L.append("")
    L.append(rule())
    L.append("Pipeline: " + " | ".join(f"{k} {v}" for k, v in
                                       sorted(counts.items(), key=lambda x: -x[1])))
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--backup", default=None)
    p.add_argument("--date", default=None, help="pretend today is YYYY-MM-DD")
    p.add_argument("--email", nargs="?", const="mpenny.ai@gmail.com", default=None)
    p.add_argument("--note", action="store_true")
    a = p.parse_args()

    bk = a.backup or newest_backup()
    data = json.load(open(bk, encoding="utf-8"))
    recs = data["data"]["files"]
    today = d(a.date) or dt.date.today()

    text = build(recs, today, a.days)
    age = dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getmtime(bk))
    hrs = age.days * 24 + age.seconds // 3600
    text += (f"\nFrom {os.path.basename(bk)}"
             f" ({hrs}h old). Read-only — nothing was changed.")

    print(text)

    subj = f"Pinewood brief — {today:%a %m/%d}"
    if a.email:
        subprocess.run([sys.executable, EMAIL_TOOL, "send", "--to", a.email,
                        "--subject", subj], input=text.encode(), check=True)
        print(f"\n[emailed to {a.email}]", file=sys.stderr)
    if a.note:
        subprocess.run([sys.executable, NOTE_TOOL, "--title", subj],
                       input=text.encode(), check=True)
        print("\n[sent to Notion Quick Notes]", file=sys.stderr)


if __name__ == "__main__":
    main()
