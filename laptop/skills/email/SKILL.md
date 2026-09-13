---
name: email
description: Read and send email from the mpenny.ai@gmail.com Gmail account via IMAP/SMTP. Use whenever Todd wants you to check the inbox, search email, read a specific message, or compose and send an email (e.g. receiving project files he's sent, or sending something to him or someone else). Triggers on phrasing like "check my email", "any new email", "read that email from X", "search my email for Y", "send an email to Z", "reply to ...", "did I get the files I sent". Read-and-send only — it does not delete, archive, or label.
---

# email

Reads and sends email for the **mpenny.ai@gmail.com** Gmail account using
Python's stdlib over IMAP (read) and SMTP (send). No third-party libraries
needed — just Python 3.

This is your own copy of a skill Penny (the WSL/terminal assistant, same
account, same laptop) also has — set up 2026-08-15 so you can send/receive
project files directly instead of routing everything through Penny. You each
use your **own separate Gmail app password** (see Configuration below) so
either can be revoked independently without affecting the other.

Capabilities: **read and send only.** This skill does not delete, archive,
move, or label messages.

## When to use

- "Check my email" / "any new email?" → `list --unread`
- "What's in my inbox?" → `list`
- "Search my email for the invoice from Acme" → `search`
- "Read that message" / "open email 12345" → `read <UID>`
- "Send an email to ..." / "email X and tell them ..." → `send`
- Todd says he emailed you files for a project → `list --unread` or `search`
  to find the message, `read <UID>` to see it and pull attachment paths

## How to run

The script needs to know where its config file is (see Configuration below —
it's **not** in the default `~/.config/...` location for this copy, since
`~` may not resolve where you expect depending on how your shell is
invoked). Set `EMAIL_CONFIG` explicitly on every call:

```bash
EMAIL_CONFIG="C:\Users\toddp\.config\email\config.json" python3 "C:\Users\toddp\.claude\skills\email\email_tool.py" <subcommand> ...
```

If you're actually running through a WSL/bash shell rather than native
PowerShell/cmd (same underlying file, different path syntax — this laptop's
`C:\` drive mounts at `/mnt/c/` in WSL), use instead:

```bash
EMAIL_CONFIG=/mnt/c/Users/toddp/.config/email/config.json python3 /mnt/c/Users/toddp/.claude/skills/email/email_tool.py <subcommand> ...
```

Try whichever matches how your other tools (the ones that already worked —
`pdftotext`, `grep`, etc.) are being invoked. Once you know which one works,
it'll always be that one for this environment.

**List recent messages** (newest first). `list` shows a `[UID]` for each:
```bash
... email_tool.py list --limit 10
... email_tool.py list --unread          # only unread
```

**Search** (accepts Gmail search syntax, e.g. `from:bob subject:invoice`):
```bash
... email_tool.py search "from:acme invoice"
```

**Read one message** by the UID shown in list/search output (attachments,
if any, get saved to a temp dir and their paths printed):
```bash
... email_tool.py read 12345
```

**Send.** For multi-line or dictated bodies, pipe via stdin to avoid quoting bugs:
```bash
... email_tool.py send --to "someone@example.com" --subject "Re: appraisal" --body "Short body."

printf '%s' "$LONG_BODY" | ... email_tool.py send --to "a@x.com,b@y.com" --cc "c@z.com" --subject "SUBJECT"
```
To attach a file: `--attach "C:\path\to\file.ext"` (repeat for multiple).
Optional: `--cc`, `--bcc`, `--from-name "Kenneth"`. Gmail automatically files
SMTP-sent mail in the Sent folder.

## IMPORTANT — sending requires confirmation

**Never send without showing Todd the exact recipient(s), subject, and full
body first, and getting an explicit go-ahead.** Sending email is outward-facing
and hard to reverse. Draft it, show it, wait for "yes/send it," then run `send`.
Reading and searching need no confirmation.

## Configuration

Your credentials live at `C:\Users\toddp\.config\email\config.json`
(`/mnt/c/Users/toddp/.config/email/config.json` from WSL) — a separate file
from Penny's, with your own dedicated Gmail app password, not shared:
```json
{
  "email": "mpenny.ai@gmail.com",
  "app_password": "<your own 16-char app password, already set>",
  "imap_host": "imap.gmail.com", "imap_port": 993,
  "smtp_host": "smtp.gmail.com", "smtp_port": 465
}
```
This has already been created and tested working (2026-08-15) — you shouldn't
need to touch it. If it ever needs replacing: generate a new app password at
https://myaccount.google.com/apppasswords (name it "Kenneth" so it's
distinguishable from Penny's in the list) and edit the file above.

## Notes
- `list`/`search`/`read` open IMAP read-only, so they never mark mail as read.
- Bodies prefer `text/plain`; HTML-only mail is crudely stripped to text.
- UIDs are stable per folder; pass `--folder` to work outside INBOX
  (e.g. `--folder "[Gmail]/Sent Mail"`).
- Attachments on `read` get saved to a fresh temp directory each time and
  the path(s) printed — read them from there.
