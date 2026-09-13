#!/usr/bin/env python3
"""Read and send email for the user's Gmail account (IMAP + SMTP).

Uses only the Python standard library. Authentication is a Gmail
**app password** (not the normal account password), stored outside this
skill dir.

Config is read from (in priority order):
  1. Environment variables EMAIL_ADDRESS and EMAIL_APP_PASSWORD
  2. A JSON config file at ~/.config/email/config.json
     (override the path with EMAIL_CONFIG)

Config file shape:
  {
    "email": "mpenny.ai@gmail.com",
    "app_password": "abcd efgh ijkl mnop",
    "imap_host": "imap.gmail.com", "imap_port": 993,
    "smtp_host": "smtp.gmail.com", "smtp_port": 465
  }

Subcommands:
  list    [--folder INBOX] [--limit 10] [--unread]
  search  "QUERY"          [--folder INBOX] [--limit 10]
  read    <UID>            [--folder INBOX]
  send    --to A --subject S --body B [--cc ...] [--bcc ...] [--from-name NAME]
"""
import argparse
import email
import email.policy
import email.utils
import imaplib
import json
import mimetypes
import os
import smtplib
import sys
from email.header import decode_header, make_header
from email.message import EmailMessage

# Windows defaults every std stream to cp1252, which breaks in both directions:
#   stdout/stderr - UnicodeEncodeError on any character outside cp1252, e.g. the
#     checkmark in cmd_send, or an em-dash inside a body printed by `read`.
#   stdin - a piped UTF-8 body is decoded as cp1252, silently turning "café"
#     into "cafÃ©" and mailing that mojibake to the recipient.
# Force UTF-8 on all three. stdin uses strict errors so malformed input fails
# loudly rather than sending a corrupted message.
for _stream, _errors in (
    (sys.stdout, "replace"),
    (sys.stderr, "replace"),
    (sys.stdin, "strict"),
):
    try:
        _stream.reconfigure(encoding="utf-8", errors=_errors)
    except (AttributeError, ValueError, OSError):
        pass  # Python < 3.7, or a stream that cannot be reconfigured.

DEFAULT_CONFIG = os.path.expanduser("~/.config/email/config.json")
DEFAULTS = {
    "imap_host": "imap.gmail.com", "imap_port": 993,
    "smtp_host": "smtp.gmail.com", "smtp_port": 465,
}


def load_config():
    cfg = dict(DEFAULTS)
    path = os.environ.get("EMAIL_CONFIG", DEFAULT_CONFIG)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    cfg["email"] = os.environ.get("EMAIL_ADDRESS", cfg.get("email"))
    cfg["app_password"] = os.environ.get("EMAIL_APP_PASSWORD", cfg.get("app_password"))
    if not cfg.get("email") or not cfg.get("app_password"):
        sys.exit(
            "ERROR: missing email credentials.\n"
            f"  Set EMAIL_ADDRESS + EMAIL_APP_PASSWORD, or fill in {path}\n"
            '  with {"email": "...", "app_password": "16-char app password"}'
        )
    return cfg


def _decode(value):
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


# ---------- IMAP (read) ----------

def imap_connect(cfg):
    try:
        M = imaplib.IMAP4_SSL(cfg["imap_host"], int(cfg["imap_port"]))
        M.login(cfg["email"], cfg["app_password"])
        return M
    except imaplib.IMAP4.error as e:
        sys.exit(
            f"ERROR: IMAP login failed: {e}\n"
            "  -> Check the app password. For Gmail, IMAP must be enabled and the\n"
            "     password must be a 16-char *app password*, not the account password."
        )


def _uid_search(M, criteria):
    typ, data = M.uid("search", None, *criteria)
    if typ != "OK":
        sys.exit(f"ERROR: IMAP search failed: {data}")
    return data[0].split()


def _fetch_headers(M, uid):
    typ, data = M.uid("fetch", uid,
                      "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
    if typ != "OK" or not data or data[0] is None:
        return None
    msg = email.message_from_bytes(data[0][1])
    return {
        "uid": uid.decode() if isinstance(uid, bytes) else str(uid),
        "from": _decode(msg.get("From")),
        "subject": _decode(msg.get("Subject")),
        "date": _decode(msg.get("Date")),
    }


def cmd_list(cfg, args):
    M = imap_connect(cfg)
    try:
        M.select(args.folder, readonly=True)
        criteria = ["UNSEEN"] if args.unread else ["ALL"]
        uids = _uid_search(M, criteria)
        uids = uids[-args.limit:][::-1]  # newest first
        if not uids:
            print("(no messages)")
            return
        for uid in uids:
            h = _fetch_headers(M, uid)
            if h:
                print(f"[{h['uid']}] {h['date']}\n    From: {h['from']}\n    Subj: {h['subject']}")
    finally:
        M.logout()


def cmd_search(cfg, args):
    M = imap_connect(cfg)
    try:
        M.select(args.folder, readonly=True)
        # Gmail supports X-GM-RAW for full search-syntax queries.
        criteria = ["X-GM-RAW", f'"{args.query}"']
        try:
            uids = _uid_search(M, criteria)
        except SystemExit:
            uids = _uid_search(M, ["TEXT", args.query])
        uids = uids[-args.limit:][::-1]
        if not uids:
            print("(no matches)")
            return
        for uid in uids:
            h = _fetch_headers(M, uid)
            if h:
                print(f"[{h['uid']}] {h['date']}\n    From: {h['from']}\n    Subj: {h['subject']}")
    finally:
        M.logout()


def _extract_body(msg):
    """Prefer text/plain; fall back to a crude HTML-to-text."""
    if msg.is_multipart():
        plain, html = None, None
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition") or "")
            if "attachment" in disp:
                continue
            if ctype == "text/plain" and plain is None:
                plain = part.get_content()
            elif ctype == "text/html" and html is None:
                html = part.get_content()
        if plain:
            return plain
        if html:
            return _strip_html(html)
        return "(no readable text body)"
    ctype = msg.get_content_type()
    payload = msg.get_content()
    return payload if ctype == "text/plain" else _strip_html(payload)


def _strip_html(html):
    import re
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", html)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    import html as _h
    return _h.unescape(text).strip()


def _save_attachments(msg, uid):
    """Save any attached/inline non-text parts to a temp dir. Returns paths."""
    if not msg.is_multipart():
        return []
    import tempfile
    saved = []
    out_dir = None
    for part in msg.walk():
        if part.is_multipart():
            continue
        ctype = part.get_content_type()
        disp = str(part.get("Content-Disposition") or "")
        filename = part.get_filename()
        is_attachment = "attachment" in disp or "inline" in disp or filename
        if ctype.startswith("text/") and not filename:
            continue
        if not is_attachment and not ctype.startswith(("image/", "application/")):
            continue
        payload = part.get_content()
        if isinstance(payload, str):
            continue  # not binary content
        if out_dir is None:
            out_dir = tempfile.mkdtemp(prefix=f"email_uid{uid}_")
        name = filename or f"part_{len(saved)}"
        name = _decode(name) or name
        path = os.path.join(out_dir, name)
        with open(path, "wb") as f:
            f.write(payload)
        saved.append(path)
    return saved


def cmd_read(cfg, args):
    M = imap_connect(cfg)
    try:
        M.select(args.folder, readonly=True)
        typ, data = M.uid("fetch", args.uid.encode(), "(RFC822)")
        if typ != "OK" or not data or data[0] is None:
            sys.exit(f"ERROR: could not fetch message UID {args.uid}")
        msg = email.message_from_bytes(data[0][1], policy=email.policy.default)
        print(f"From:    {_decode(msg.get('From'))}")
        print(f"To:      {_decode(msg.get('To'))}")
        print(f"Date:    {_decode(msg.get('Date'))}")
        print(f"Subject: {_decode(msg.get('Subject'))}")
        print("-" * 60)
        print(_extract_body(msg))
        attachments = _save_attachments(msg, args.uid)
        if attachments:
            print("-" * 60)
            print("Attachments saved:")
            for path in attachments:
                print(f"  {path}")
    finally:
        M.logout()


# ---------- SMTP (send) ----------

def cmd_send(cfg, args):
    body = args.body
    if body is None:
        body = sys.stdin.read()
    if not (args.to and args.subject and body.strip()):
        sys.exit("ERROR: send needs --to, --subject, and a body (--body or stdin).")

    msg = EmailMessage()
    from_name = args.from_name
    msg["From"] = email.utils.formataddr((from_name, cfg["email"])) if from_name else cfg["email"]
    msg["To"] = args.to
    if args.cc:
        msg["Cc"] = args.cc
    msg["Subject"] = args.subject
    msg.set_content(body)

    for path in (args.attach or []):
        if not os.path.isfile(path):
            sys.exit(f"ERROR: attachment not found: {path}")
        ctype, _ = mimetypes.guess_type(path)
        maintype, subtype = (ctype.split("/", 1) if ctype else ("application", "octet-stream"))
        with open(path, "rb") as fh:
            msg.add_attachment(fh.read(), maintype=maintype, subtype=subtype,
                               filename=os.path.basename(path))

    recipients = [a.strip() for a in args.to.split(",") if a.strip()]
    if args.cc:
        recipients += [a.strip() for a in args.cc.split(",") if a.strip()]
    if args.bcc:
        recipients += [a.strip() for a in args.bcc.split(",") if a.strip()]

    try:
        with smtplib.SMTP_SSL(cfg["smtp_host"], int(cfg["smtp_port"])) as s:
            s.login(cfg["email"], cfg["app_password"])
            s.send_message(msg, from_addr=cfg["email"], to_addrs=recipients)
    except smtplib.SMTPAuthenticationError:
        sys.exit("ERROR: SMTP auth failed. Check the app password (16-char, not the account password).")
    except smtplib.SMTPException as e:
        sys.exit(f"ERROR: sending failed: {e}")

    print(f"✅ Sent to {args.to}" + (f" (cc {args.cc})" if args.cc else ""))
    print(f"   Subject: {args.subject}")
    if args.attach:
        print(f"   Attachments: {', '.join(os.path.basename(a) for a in args.attach)}")


def main():
    ap = argparse.ArgumentParser(description="Read and send Gmail via IMAP/SMTP.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="List recent messages.")
    p.add_argument("--folder", default="INBOX")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--unread", action="store_true", help="Only unread messages.")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("search", help="Search messages (Gmail search syntax).")
    p.add_argument("query")
    p.add_argument("--folder", default="INBOX")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("read", help="Print one message by UID.")
    p.add_argument("uid")
    p.add_argument("--folder", default="INBOX")
    p.set_defaults(func=cmd_read)

    p = sub.add_parser("send", help="Send a message.")
    p.add_argument("--to", required=True, help="Comma-separated recipients.")
    p.add_argument("--subject", required=True)
    p.add_argument("--body", default=None, help="Body text (or pipe via stdin).")
    p.add_argument("--cc", default=None)
    p.add_argument("--bcc", default=None)
    p.add_argument("--from-name", default=None, help="Display name for the From header.")
    p.add_argument("--attach", action="append", default=None,
                   help="File path to attach (repeat for multiple).")
    p.set_defaults(func=cmd_send)

    args = ap.parse_args()
    cfg = load_config()
    args.func(cfg, args)


if __name__ == "__main__":
    main()
