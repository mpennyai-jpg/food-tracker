#!/usr/bin/env python3
"""
build_workup.py — wrap a workup body fragment in the scrollable reading shell.

Authoring stays exactly as it was: write the body with <div class="part">...</div>
part dividers and <h2>/<h3> headings. This script does the rest — wraps each h2
into a collapsible <section>, builds the sidebar nav from the headings, adds the
screen CSS, the font-size control, the filter box, and the print CSS that puts the
document back into the 10.5pt letterhead form for the PDF.

  python3 build_workup.py --out "<addr> - WORKUP.html" \
      --heading "Pre-Report Workup — <addr>" --sub "<subtitle line>" \
      --body body.html [--logo pinewood-logo.png] [--title "<tab title>"]

Body fragment may also pull in whole workfile .txt files:
      --workfile "Part 3 label::/path/to/FILE.txt"   (repeatable)
"""
import argparse, base64, html, os, re, sys

# ---------------------------------------------------------------- text -> html

def txt_to_html(path):
    """Convert a Pinewood workfile .txt into h2/h3 + <pre> blocks.

    Preserves column alignment exactly — these files carry hand-aligned tables
    and a reflow would mangle them. Headings are detected from the two rule
    styles the workfiles use: a line boxed by ==== rules, and a line underlined
    by ---- .
    """
    raw = open(path, encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
    lines = raw.split('\n')
    out, buf = [], []

    def flush():
        while buf and not buf[-1].strip():
            buf.pop()
        while buf and not buf[0].strip():
            buf.pop(0)
        if buf:
            out.append('<pre class="tx">' + html.escape('\n'.join(buf)) + '</pre>')
        buf.clear()

    def isrule(s, ch):
        t = s.strip()
        return len(t) >= 4 and set(t) == {ch}

    i, first = 0, True
    while i < len(lines):
        ln = lines[i]
        # ==== / heading / ====   or   heading followed by ====
        if isrule(ln, '=') and i + 2 < len(lines) and lines[i + 1].strip() and isrule(lines[i + 2], '='):
            flush(); out.append('<h3>' + html.escape(lines[i + 1].strip()) + '</h3>'); i += 3; continue
        if isrule(ln, '=') and i + 1 < len(lines) and lines[i + 1].strip() and not isrule(lines[i + 1], '='):
            # opening rule of a boxed heading whose closing rule follows the text
            j = i + 1
            while j < len(lines) and lines[j].strip() and not isrule(lines[j], '='):
                j += 1
            if j < len(lines) and isrule(lines[j], '='):
                flush()
                out.append('<h3>' + html.escape(' '.join(l.strip() for l in lines[i + 1:j])) + '</h3>')
                i = j + 1; continue
        # heading underlined by ---- or ====  (may wrap over 2-3 lines)
        if ln.strip() and i + 1 < len(lines) and (isrule(lines[i + 1], '-') or isrule(lines[i + 1], '=')) \
                and len(ln.strip()) < 100 and not first:
            head = [ln.strip()]
            # pull back contiguous non-blank lines that belong to the same heading
            while len(head) < 3 and buf and buf[-1].strip() and len(buf[-1].strip()) < 100 \
                    and len(' '.join(head)) + len(buf[-1].strip()) < 170:
                head.insert(0, buf.pop().strip())
                if re.match(r'^(\d+[.)]|[A-Z][A-Z ]{2,})', head[0]):
                    break
            flush(); out.append('<h3>' + html.escape(' '.join(head)) + '</h3>'); i += 2; continue
        if first and ln.strip():
            first = False
        buf.append(ln); i += 1
    flush()
    return '\n'.join(out)


# ------------------------------------------------------------ section wrapping

def plain(s):
    """Tag-stripped, entity-decoded text of an HTML fragment."""
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def slug(s, used):
    b = re.sub(r'[^a-z0-9]+', '-', plain(s).lower()).strip('-')[:48] or 'sec'
    s2, n = b, 2
    while s2 in used:
        s2 = f'{b}-{n}'; n += 1
    used.add(s2)
    return s2


def wrap_sections(body):
    """Split the fragment at <div class="part"> and <h2> and rebuild it as
    collapsible sections. Returns (html, nav_tree)."""
    tok = re.split(r'(<div class="part"[^>]*>.*?</div>|<h2[^>]*>.*?</h2>)', body,
                   flags=re.S | re.I)
    used, nav, out = set(), [], []
    open_sec = False
    lead = tok[0]

    def close():
        nonlocal open_sec
        if open_sec:
            out.append('</div></section>')
            open_sec = False

    i = 1
    while i < len(tok):
        marker, content = tok[i], tok[i + 1] if i + 1 < len(tok) else ''
        inner = re.sub(r'<[^>]+>', '', marker).strip()   # keeps entities for display
        label = plain(marker)                                # decoded, for nav + ids
        if 'class="part"' in marker.lower():
            close()
            pid = slug('part-' + label, used)
            out.append(f'<div class="part" id="{pid}">{inner}</div>')
            nav.append({'kind': 'part', 'id': pid, 'text': label, 'kids': []})
        else:
            close()
            sid = slug(label, used)
            subs = []
            for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', content, flags=re.S | re.I):
                t = plain(m.group(1))
                if t:
                    subs.append({'id': slug(t, used), 'text': t})
            # stamp ids onto the h3s in order
            it = iter(subs)
            def stamp(m):
                try:
                    s = next(it)
                except StopIteration:
                    return m.group(0)
                return f'<h3 id="{s["id"]}">' + m.group(1) + '</h3>'
            content = re.sub(r'<h3[^>]*>(.*?)</h3>', stamp, content, flags=re.S | re.I)

            out.append(f'<section class="sec" id="{sid}">'
                       f'<h2 class="sechead" tabindex="0" role="button" aria-expanded="true">'
                       f'<span class="chev" aria-hidden="true"></span>{inner}</h2>'
                       f'<div class="secbody">')
            open_sec = True
            out.append(content)
            entry = {'kind': 'sec', 'id': sid, 'text': label, 'kids': subs}
            if nav and nav[-1]['kind'] == 'part':
                nav[-1]['kids'].append(entry)
            else:
                nav.append(entry)
        i += 2
    close()
    return lead + '\n'.join(out), nav


def render_nav(nav):
    o = []
    for n in nav:
        if n['kind'] == 'part':
            o.append(f'<div class="navpart"><a href="#{n["id"]}">{html.escape(n["text"])}</a></div>')
            for s in n['kids']:
                o.append(navsec(s))
        else:
            o.append(navsec(n))
    return '\n'.join(o)


def navsec(s):
    o = [f'<a class="navsec" href="#{s["id"]}" data-t="{s["id"]}">{html.escape(s["text"])}</a>']
    if s['kids']:
        o.append('<div class="navsubs">')
        for k in s['kids']:
            o.append(f'<a class="navsub" href="#{k["id"]}" data-t="{k["id"]}">{html.escape(k["text"])}</a>')
        o.append('</div>')
    return '\n'.join(o)


# ------------------------------------------------------------------- the shell

CSS = r"""
:root{ --fs:16px; --ink:#1a1a1a; --blue:#0F4761; --rule:#c8d4da; --bg:#ffffff;
       --side:#f4f7f9; --measure:66rem; }
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{ margin:0; background:var(--bg); color:var(--ink); font-size:var(--fs);
      font-family:"Segoe UI",Arial,sans-serif; line-height:1.55; }

/* ---- top bar ---- */
.topbar{ position:sticky; top:0; z-index:40; display:flex; align-items:center; gap:14px;
  background:var(--blue); color:#fff; padding:8px 16px; font-size:.88rem; }
.topbar .addr{ font-weight:600; font-size:1rem; margin-right:auto;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.topbar button{ font:inherit; background:rgba(255,255,255,.14); color:#fff;
  border:1px solid rgba(255,255,255,.35); border-radius:5px; padding:4px 11px; cursor:pointer; }
.topbar button:hover{ background:rgba(255,255,255,.28) }
.topbar .fsz{ display:flex; align-items:center; gap:5px }
.topbar .fsz b{ font-weight:600; opacity:.8; font-size:.8rem }

/* ---- layout ---- */
.wrap{ display:flex; align-items:flex-start; }
nav.side{ position:sticky; top:41px; flex:0 0 20rem; max-height:calc(100vh - 41px);
  overflow-y:auto; background:var(--side); border-right:1px solid var(--rule);
  padding:12px 10px 40px; font-size:.87rem; }
nav.side .find{ width:100%; font:inherit; font-size:.9rem; padding:6px 9px; margin-bottom:8px;
  border:1px solid var(--rule); border-radius:5px; background:#fff; }
nav.side .navpart{ margin:14px 0 5px; font-weight:700; color:var(--blue);
  font-size:.82rem; letter-spacing:.02em; text-transform:uppercase; }
nav.side .navpart a{ color:inherit; text-decoration:none }
nav.side a{ display:block; color:#24404c; text-decoration:none; padding:4px 8px;
  border-radius:5px; border-left:3px solid transparent; }
nav.side a.navsec:hover,nav.side a.navsub:hover{ background:#e2ebf0 }
nav.side a.on{ background:#dce8ee; border-left-color:var(--blue); font-weight:600; color:var(--blue) }
nav.side .navsubs{ margin:1px 0 3px 10px; border-left:1px solid var(--rule); padding-left:4px }
nav.side .navsub{ font-size:.82rem; color:#4a6069; padding:3px 8px }
nav.side .hidden{ display:none }

main{ flex:1 1 auto; min-width:0; padding:6px 40px 60vh; }
.doc{ max-width:var(--measure); }

/* ---- letterhead ---- */
.letterhead{ text-align:center; margin:14px 0 2px } .letterhead img{ height:74px }
.contact{ font-size:.8rem; color:#3a3a3a; margin-bottom:12px }
h1{ color:var(--blue); font-size:1.5rem; margin:6px 0 2px; line-height:1.25 }
.sub{ color:#4a4a4a; font-size:.9rem; margin-bottom:12px }

/* ---- sections ---- */
.part{ color:var(--blue); font-size:1.12rem; font-weight:700; border-bottom:2px solid var(--blue);
  margin:34px 0 4px; padding-bottom:3px; scroll-margin-top:52px; }
.sec{ border-bottom:1px solid #e3e9ec; scroll-margin-top:52px; }
h2.sechead{ color:var(--blue); font-size:1.12rem; margin:0; padding:13px 0 11px 26px;
  position:relative; cursor:pointer; user-select:none; line-height:1.3; }
h2.sechead:hover{ color:#15617f }
h2.sechead:focus-visible{ outline:2px solid var(--blue); outline-offset:2px }
.chev{ position:absolute; left:4px; top:1.05em; width:0; height:0;
  border-left:6px solid currentColor; border-top:5px solid transparent;
  border-bottom:5px solid transparent; transform:rotate(90deg); transition:transform .12s; }
.sec.shut .chev{ transform:rotate(0deg) }
.sec.shut .secbody{ display:none }
.secbody{ padding:0 0 20px 26px }
h3{ color:var(--blue); font-size:1rem; margin:20px 0 5px; scroll-margin-top:52px }

/* ---- content ---- */
table{ border-collapse:collapse; width:100%; margin:9px 0; font-size:.9rem }
thead{ display:table-header-group }
th,td{ border:1px solid #b9c6cc; padding:5px 8px; text-align:left; vertical-align:top }
th{ background:#eef3f6 } .num{ text-align:right }
tbody tr:nth-child(even){ background:#fafcfd }
.tblwrap{ overflow-x:auto }
ul{ margin:6px 0 6px 20px; padding:0 } li{ margin:3px 0 }
.callout{ border:1px solid var(--blue); border-left-width:5px; background:#f4f8fa;
  padding:11px 14px; margin:12px 0; border-radius:0 5px 5px 0; }
.warn{ border-color:#8a2c02; background:#fdf3ee }
.plain{ border:1px solid #b6cdb6; border-left:5px solid #4a7c4a; background:#f3f8f3;
  padding:10px 14px; margin:10px 0; border-radius:0 5px 5px 0; font-size:.94rem }
.plain::before{ content:"In plain terms"; display:block; font-weight:700; color:#356135;
  font-size:.76rem; letter-spacing:.05em; text-transform:uppercase; margin-bottom:3px }
pre.tx{ font-family:"Cascadia Mono",Consolas,"Courier New",monospace; font-size:.85rem;
  line-height:1.5; white-space:pre; overflow-x:auto; background:#fbfcfd;
  border:1px solid #e4eaed; border-radius:5px; padding:11px 13px; margin:9px 0; }
mark{ background:#ffe9a8; padding:0 1px }
.todo{ background:#fff2cc; border:1px dashed #b8892b; color:#7a5a10; border-radius:4px;
  padding:0 6px; font-size:.86em; font-style:italic; white-space:nowrap }
code{ font-family:Consolas,"Courier New",monospace; font-size:.92em;
  background:#eef2f4; padding:1px 5px; border-radius:3px }
.dim{ opacity:.32 }

/* ---- print: back to the 10.5pt letterhead document ---- */
@media print{
  @page{ margin:.5in }
  :root{ --fs:10.5pt; --measure:none }
  body{ font-size:10.5pt; line-height:1.32 }
  .topbar,nav.side{ display:none !important }
  .wrap{ display:block } main{ padding:0 } .doc{ max-width:none }
  .sec.shut .secbody{ display:block !important }
  .chev{ display:none } h2.sechead{ padding-left:0; font-size:12pt; cursor:auto }
  .secbody{ padding-left:0 }
  .sec{ border-bottom:none }
  h1{ font-size:15pt } h3{ font-size:10.8pt }
  .part{ font-size:13pt; margin-top:16px }
  table,.callout,.plain{ page-break-inside:avoid }
  th,td{ font-size:9.5pt; padding:2.5px 5px }
  pre.tx{ font-size:8.6pt; white-space:pre-wrap; page-break-inside:auto }
  .dim{ opacity:1 }
  .todo{ background:none; border:none; padding:0 }
}
"""

JS = r"""
(function(){
  var K='workup:'+document.title;
  var secs=[].slice.call(document.querySelectorAll('.sec'));
  var links=[].slice.call(document.querySelectorAll('nav.side a[data-t]'));

  // ---- collapse / expand, remembered per document
  var shut={}; try{ shut=JSON.parse(localStorage.getItem(K+':shut')||'{}'); }catch(e){}
  secs.forEach(function(s){
    if(shut[s.id]) s.classList.add('shut');
    var h=s.querySelector('.sechead');
    h.setAttribute('aria-expanded', String(!s.classList.contains('shut')));
    function tog(){
      s.classList.toggle('shut');
      var open=!s.classList.contains('shut');
      h.setAttribute('aria-expanded',String(open));
      shut[s.id]=!open; save();
    }
    h.addEventListener('click',tog);
    h.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){ e.preventDefault(); tog(); }
    });
  });
  function save(){ try{ localStorage.setItem(K+':shut',JSON.stringify(shut)); }catch(e){} }
  function setAll(open){
    secs.forEach(function(s){
      s.classList.toggle('shut',!open); shut[s.id]=!open;
      s.querySelector('.sechead').setAttribute('aria-expanded',String(open));
    });
    save();
  }
  document.getElementById('xall').addEventListener('click',function(){ setAll(true); });
  document.getElementById('call').addEventListener('click',function(){ setAll(false); });

  // ---- font size
  var fs=parseFloat(localStorage.getItem(K+':fs')||'16');
  function apply(){
    fs=Math.min(24,Math.max(12,fs));
    document.documentElement.style.setProperty('--fs',fs+'px');
    try{ localStorage.setItem(K+':fs',fs); }catch(e){}
  }
  apply();
  document.getElementById('fsup').addEventListener('click',function(){ fs+=1; apply(); });
  document.getElementById('fsdn').addEventListener('click',function(){ fs-=1; apply(); });

  // ---- find: expands every section that contains the term, dims the rest
  var box=document.getElementById('find');
  var hits=document.getElementById('hits');
  box.addEventListener('input',function(){
    var q=box.value.trim().toLowerCase();
    if(!q){
      secs.forEach(function(s){
        s.classList.remove('dim');
        s.classList.toggle('shut',!!shut[s.id]);
      });
      links.forEach(function(a){ a.classList.remove('hidden'); });
      hits.textContent=''; return;
    }
    var n=0, ids={};
    secs.forEach(function(s){
      var hit=s.textContent.toLowerCase().indexOf(q)>=0;
      s.classList.toggle('dim',!hit);
      s.classList.toggle('shut',!hit);
      if(hit){ n++; ids[s.id]=1; }
    });
    links.forEach(function(a){
      var sec=a.getAttribute('data-t');
      var host=document.getElementById(sec);
      var owner=host&&host.closest?host.closest('.sec'):null;
      a.classList.toggle('hidden',!(ids[sec]||(owner&&ids[owner.id])));
    });
    hits.textContent=n+(n===1?' section':' sections');
  });
  box.addEventListener('keydown',function(e){ if(e.key==='Escape'){ box.value=''; box.dispatchEvent(new Event('input')); }});

  // ---- scroll-spy
  var targets=[].slice.call(document.querySelectorAll('.sec, h3[id]'));
  var byId={}; links.forEach(function(a){ byId[a.getAttribute('data-t')]=a; });
  var seen={};
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ seen[e.target.id]=e.isIntersecting?e.boundingClientRect.top:null; });
    var best=null;
    targets.forEach(function(t){
      var r=t.getBoundingClientRect();
      if(r.top<=140 && r.bottom>60){ if(!best||r.top>best.getBoundingClientRect().top) best=t; }
    });
    links.forEach(function(a){ a.classList.remove('on'); });
    if(best&&byId[best.id]){
      byId[best.id].classList.add('on');
      var a=byId[best.id], nv=document.querySelector('nav.side');
      var ar=a.getBoundingClientRect(), nr=nv.getBoundingClientRect();
      if(ar.top<nr.top+8||ar.bottom>nr.bottom-8) a.scrollIntoView({block:'nearest'});
    }
  },{rootMargin:'-60px 0px -55% 0px',threshold:[0,1]});
  targets.forEach(function(t){ io.observe(t); });

  // ---- a link into a collapsed section opens it
  document.querySelectorAll('nav.side a').forEach(function(a){
    a.addEventListener('click',function(){
      var id=a.getAttribute('href').slice(1), el=document.getElementById(id);
      var sec=el&&el.closest?el.closest('.sec'):null;
      if(sec&&sec.classList.contains('shut')){
        sec.classList.remove('shut'); shut[sec.id]=false; save();
        sec.querySelector('.sechead').setAttribute('aria-expanded','true');
      }
    });
  });
  window.addEventListener('beforeprint',function(){ setAll(true); });
})();
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>

<div class="topbar">
  <span class="addr">{addr}</span>
  <span class="fsz"><b>Text</b>
    <button id="fsdn" title="Smaller text">A&minus;</button>
    <button id="fsup" title="Larger text">A+</button></span>
  <button id="xall">Expand all</button>
  <button id="call">Collapse all</button>
  <button onclick="window.print()">Print / PDF</button>
</div>

<div class="wrap">
<nav class="side">
  <input id="find" class="find" type="search" placeholder="Filter sections…" aria-label="Filter sections">
  <div id="hits" style="font-size:.78rem;color:#5b7480;min-height:1.1em;margin:-4px 0 6px 2px"></div>
{nav}
</nav>
<main><div class="doc">
{letterhead}
<h1>{heading}</h1>
<div class="sub">{sub}</div>
{body}
</div></main>
</div>

<script>{js}</script>
</body>
</html>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    p.add_argument('--body', required=True, help='HTML fragment: <div class="part">/<h2>/<h3>')
    p.add_argument('--heading', required=True)
    p.add_argument('--sub', default='')
    p.add_argument('--title', default=None)
    p.add_argument('--addr', default=None, help='short label for the sticky bar')
    p.add_argument('--logo', default=None)
    p.add_argument('--logo-uri', default=None, help='reuse a base64 data URI')
    p.add_argument('--workfile', action='append', default=[],
                   help='"Section heading::/path/file.txt" appended as its own section')
    a = p.parse_args()

    body = open(a.body, encoding='utf-8', errors='replace').read()
    for spec in a.workfile:
        head, _, path = spec.partition('::')
        if not path or not os.path.exists(path):
            print(f'  ! workfile missing, skipped: {spec}', file=sys.stderr); continue
        body += f'\n<h2>{html.escape(head)}</h2>\n' + txt_to_html(path) + '\n'

    wrapped, nav = wrap_sections(body)

    lh = ''
    uri = a.logo_uri
    if not uri and a.logo and os.path.exists(a.logo):
        uri = 'data:image/png;base64,' + base64.b64encode(open(a.logo, 'rb').read()).decode()
    if uri:
        lh = (f'<div class="letterhead"><img src="{uri}" alt="Pinewood Appraisal"></div>\n'
              '<div class="contact">Todd A. Paris | P.O. Box 330326 | Murfreesboro, TN 37133-0326<br>'
              'Phone: (615) 956-2099 | Email: PinewoodAppraisal@gmail.com</div>')

    page = PAGE.format(
        title=html.escape(a.title or a.heading), css=CSS, js=JS,
        addr=html.escape(a.addr or a.title or a.heading),
        nav=render_nav(nav), letterhead=lh,
        heading=a.heading, sub=a.sub, body=wrapped)
    open(a.out, 'w', encoding='utf-8').write(page)
    nsec = sum(1 + len(n['kids']) if n['kind'] == 'part' else 1 for n in nav)
    print(f'wrote {a.out}  ({len(page):,} bytes, {len(nav)} nav groups, '
          f'{len(re.findall(chr(60)+"section", page))} sections)')


if __name__ == '__main__':
    main()
