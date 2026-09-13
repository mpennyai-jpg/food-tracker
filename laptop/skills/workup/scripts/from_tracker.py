#!/usr/bin/env python3
"""
from_tracker.py — build the Part 1 skeleton of a workup straight off a tracker record.

The workup document should exist the moment an order lands, not the day the
analysis is done. This reads the newest Appraisal Tracker auto-backup, matches a
record on street number + street name, and writes:

  * a body fragment with Part 1 sections 1-3 filled in (assignment, contract,
    subject public record) and every unknown shown as an open slot, and
  * any attachments on the record (order sheet, sales contract, bids) written out
    as real files.

Sections 4-5 and Parts 2-3 get appended by the workup and the narrative skills as
the file progresses. Re-run it any time and it re-reads the current record.

  python3 from_tracker.py "739 Lakeview" --out body.html [--attach-dir DIR]
  python3 from_tracker.py --list
"""
import argparse, base64, datetime as dt, glob, html, json, os, re, sys

BACKUPS = "/mnt/c/Users/toddp/OneDrive/Appraisal Tracker/Appraisal Tracker - Backups"
TODO = '<span class="todo">not supplied yet</span>'


def newest_backup(d=BACKUPS):
    fs = sorted(glob.glob(os.path.join(d, "appraisal-tracker-auto-*.json")), key=os.path.getmtime)
    if not fs:
        sys.exit(f"no auto-backup found in {d}")
    return fs[-1]


def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', (s or '').lower()).strip()


def find(recs, frag):
    f = norm(frag)
    hits = [r for r in recs if f in norm(f"{r.get('address','')} {r.get('city','')}")]
    if not hits:                       # fall back to street number + first word
        p = f.split()
        if p:
            hits = [r for r in recs if norm(r.get('address', '')).startswith(p[0])]
    return hits


def e(v):
    """Escape a value, or render the open-slot marker when it is empty."""
    s = '' if v is None else str(v).strip()
    return html.escape(s) if s else TODO


def money(v):
    try:
        return '$' + f'{float(str(v).replace("$", "").replace(",", "")):,.0f}'
    except (TypeError, ValueError):
        return e(v)


def date(v):
    try:
        return dt.datetime.strptime(str(v)[:10], '%Y-%m-%d').strftime('%m/%d/%Y')
    except (TypeError, ValueError):
        return e(v)


def rows(pairs):
    out = ['<table><tbody>']
    for k, v in pairs:
        out.append(f'<tr><td style="width:11rem">{html.escape(k)}</td><td>{v}</td></tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)


def build(r, backup_name):
    pub = r.get('pub') or {}
    par, geo, fld = pub.get('parcel') or {}, pub.get('geo') or {}, pub.get('flood') or {}
    con = r.get('contract') or {}
    addr = ' '.join(x for x in [r.get('address'), r.get('city'), r.get('statezip')] if x)
    purchase = bool(con.get('contractDate') or con.get('buyers') or con.get('price'))
    o = []

    o.append('<div class="part">Part 1 — The report information</div>')

    o.append('<h2>1. Assignment</h2>')
    o.append(rows([
        ('Order / Loan', f"{e(r.get('orderNo'))} / {e(r.get('loanNo'))}"),
        ('Client / AMC', f"{e(r.get('amc'))} · lender {e(r.get('lender'))}"),
        ('Borrower', e(r.get('borrower'))),
        ('Product', f"{e(r.get('product'))}{' · ' + html.escape(r['loanType']) if r.get('loanType') else ''}"
                    f"{' · ' + html.escape(r['assignmentType']) if r.get('assignmentType') else ''}"),
        ('Property', f"{e(addr)} · {e(r.get('county'))} County"),
        ('Ordered', date(r.get('orderDate'))),
        ('Inspection', f"{date(r.get('inspectionDate'))} {html.escape(r.get('inspectionTime') or '')}".strip()),
        ('Due', f'<b>{date(r.get("dueDate"))}</b>'),
        ('Fee', money(r.get('fee'))),
        ('Status', e(r.get('status'))),
    ]))
    notes = [n.get('text', '') for n in (r.get('notes') or []) if n.get('text')]
    if notes:
        o.append('<div class="callout"><b>Order notes.</b><ul>'
                 + ''.join(f'<li>{html.escape(t)}</li>' for t in notes) + '</ul></div>')
    atts = [a.get('name', '') for a in (r.get('attachments') or [])]
    o.append('<p><b>On the order:</b> '
             + (', '.join(html.escape(a) for a in atts) if atts else TODO) + '</p>')

    if purchase:
        o.append('<h2>2. Contract items to address</h2>')
        stip = con.get('stipulations') or []
        o.append(rows([
            ('Price', money(con.get('price'))),
            ('Binding date', date(con.get('contractDate'))),
            ('Closing', date(con.get('closingDate'))),
            ('Buyers', e(con.get('buyers'))),
            ('Sellers', e(con.get('sellers'))
                        + (f' — <b>check against owner of record:</b> {html.escape(par["owner"])}'
                           if par.get('owner') else '')),
            ('Financing', e(con.get('financing'))),
            ('Earnest', money(con.get('earnest'))),
            ('Concessions', (html.escape(con['concessions']) if con.get('concessions')
                             else '<b>none stated in the contract block</b> — confirm against the signed pages')),
            ('Closing costs', e(con.get('closingCosts'))),
            ('Personal property', e(con.get('personalProperty'))),
            ('Stipulations', ('<br>'.join(html.escape(s) for s in stip) if stip else TODO)),
            ('PUD / HOA', f"{e(con.get('pud'))} · {e(con.get('hoaName'))} "
                          f"{html.escape(str(con.get('hoaDues') or ''))} {html.escape(str(con.get('hoaPeriod') or ''))}"),
        ]))
        o.append('<div class="callout warn"><b>Contract block is the tracker parse, not the signed pages.</b> '
                 'Run <code>sales-contract-analysis</code> on the contract PDF and replace this section with its '
                 'output before anything downstream uses the price, the binding date, or the concessions.</div>')

    o.append('<h2>3. Subject — public record</h2>')
    if par or geo or fld:
        o.append(rows([
            ('Parcel / APN', e(par.get('apn'))),
            ('Owner of record', e(par.get('owner'))),
            ('Subdivision / lot', f"{e(par.get('subdiv'))} · lot {e(par.get('lot'))} · plat {e(par.get('plat'))}"),
            ('Deed', e(par.get('deed'))),
            ('Year built', e(par.get('yearBuilt'))),
            ('Assessor area', (f"{int(par['sqft']):,} sf" if par.get('sqft') else TODO)
                              + ' — <b>screen only, measure governs</b>'),
            ('Type / stories', f"{e(par.get('bldgType'))} · {e(par.get('stories'))}"),
            ('Site', (f"{float(par['acres']):.3f} ac" if par.get('acres') else TODO)),
            ('Assessor values', f"total {money(par.get('valTotal'))} · land {money(par.get('valLand'))} · "
                                f"bldg {money(par.get('valBldg'))} · assessed {money(par.get('assessed'))}"),
            ('Last recorded sale', money(par.get('salePrice'))),
            ('Census tract / setting', f"{e(geo.get('tract'))} · {e(geo.get('urban'))}"),
            ('Coordinates', (f"{geo['lat']:.6f}, {geo['lon']:.6f} — use these for the distance column"
                             if geo.get('lat') else TODO)),
            ('Flood', f"Zone {e(fld.get('zone'))} · {e(fld.get('subty'))} · SFHA {e(fld.get('sfha'))} · "
                      f"panel {e(fld.get('panel'))} eff {e(fld.get('eff'))}"),
            ('Source', f"{e(par.get('src'))}, pulled "
                       + (dt.datetime.fromtimestamp(pub['ranAt'] / 1000).strftime('%m/%d/%Y')
                          if pub.get('ranAt') else TODO)),
        ]))
    else:
        o.append('<div class="callout warn"><b>No public-record block on this order yet.</b> '
                 'Run the tracker\'s public-records pull. Until it exists there is no parcel number, no owner of '
                 'record to check the seller against, no assessor area to screen GLA against, no flood zone, and '
                 'no census tract — and four of the six narrative sections need those.</div>')

    o.append('<h2>4. Report narratives — form-ready</h2>')
    o.append('<div class="callout"><b>Nothing here yet.</b> This section fills as the narrative skills run: '
             'neighborhood form entries and boundaries, market conditions comment, highest and best use, '
             'exposure time, marketing time, and the as-is site-improvements number. '
             'Paste from the REPORT .txt files in the job folder, not from this PDF.</div>')

    o.append('<h2>5. Items to resolve before delivery</h2>')
    open_items = []
    if not (par or geo):
        open_items.append('Public-records pull has not run on this order.')
    if purchase and not con.get('price'):
        open_items.append('Contract price is blank in the tracker parse — read it off the signed pages.')
    if purchase and not (con.get('concessions') or '').strip():
        open_items.append('Concessions field is empty. Empty is not the same as none — confirm on the contract, '
                          'and run the IPC test if this is FHA or VA.')
    status = (r.get('status') or '').lower()
    if not r.get('inspectionDate'):
        if status in ('inspected', 'in progress', 'draft', 'delivered', 'complete'):
            open_items.append(f'Status says "{r.get("status")}" but the record carries no inspection date. '
                              'The effective date is the inspection date — get it off his calendar or his notes '
                              'before any time-sensitive conclusion is written, and fix the tracker record.')
        else:
            open_items.append('No inspection date set, so the effective date is provisional and every '
                              'time-sensitive conclusion re-anchors when it is set.')
    if not atts:
        open_items.append('No attachments on the order record — the order sheet and any contract are missing.')
    open_items.append('MLS closed export — nothing in Part 2 can run without it.')
    open_items.append('Active and pending export — without it marketing time is a disclosed assumption, '
                      'not a finding.')
    open_items.append('His inspection observations — condition and quality ratings, and the site-improvements '
                      'inventory, are his observation only.')
    o.append('<ul>' + ''.join(f'<li>{html.escape(t)}</li>' for t in open_items) + '</ul>')
    o.append(f'<p class="sub">Skeleton built from <code>{html.escape(backup_name)}</code> on '
             f'{dt.datetime.now():%m/%d/%Y %I:%M %p}. Re-run <code>from_tracker.py</code> to refresh it.</p>')
    return '\n'.join(o), addr


def main():
    p = argparse.ArgumentParser()
    p.add_argument('address', nargs='?', help='street number + street name fragment')
    p.add_argument('--out', default='body.html')
    p.add_argument('--attach-dir', default=None, help='write the record attachments here')
    p.add_argument('--backup', default=None)
    p.add_argument('--list', action='store_true', help='list recent tracker records')
    a = p.parse_args()

    bk = a.backup or newest_backup()
    d = json.load(open(bk, encoding='utf-8'))
    recs = d['data']['files']

    if a.list or not a.address:
        for r in sorted(recs, key=lambda r: r.get('orderDate') or '', reverse=True)[:25]:
            print(f"  {r.get('orderDate','----------')}  {r.get('status',''):<12} "
                  f"{r.get('address','')}, {r.get('city','')}  [{r.get('amc','')}]")
        return

    hits = find(recs, a.address)
    if not hits:
        sys.exit(f'no tracker record matching "{a.address}" in {os.path.basename(bk)}')
    if len(hits) > 1:
        print('matched more than one — be more specific:', file=sys.stderr)
        for r in hits:
            print(f"  {r.get('address')}, {r.get('city')} ({r.get('orderDate')})", file=sys.stderr)
        sys.exit(1)
    r = hits[0]

    body, addr = build(r, os.path.basename(bk))
    open(a.out, 'w', encoding='utf-8').write(body)
    print(f'wrote {a.out}  — {addr}')

    if a.attach_dir:
        os.makedirs(a.attach_dir, exist_ok=True)
        for at in r.get('attachments') or []:
            blob = d.get('attachments', {}).get(at['id'])
            if not blob:
                print(f'  ! no blob for {at["name"]}'); continue
            dest = os.path.join(a.attach_dir, at['name'])
            open(dest, 'wb').write(base64.b64decode(blob.split(',', 1)[1]))
            print(f'  attachment -> {dest}')

    miss = body.count(TODO)
    print(f'  {miss} open slot(s) in Part 1')
    print(f'  age of backup: {(dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getmtime(bk))).seconds // 3600}h '
          f'— the tracker can be up to six hours ahead of it')


if __name__ == '__main__':
    main()
