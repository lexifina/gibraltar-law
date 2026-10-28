"""Builds a git repository of Gibraltar law from the Gibraltar Laws website (www.gibraltarlaws.gov.gi), in which every
amending enactment is one commit, dated the day it took effect.

    python -X utf8 scripts/gibraltar-law/build.py [--repo ../gibraltar-law] [--today 2026-10-28] [--offline]
                                                  [--verify-rebuild]

The Government of Gibraltar's site publishes each act in each of its dated versions as a PDF, and each PDF opens with a
table of the amending enactments, the provisions they affect and the day each took effect. We read the PDFs with
PyMuPDF, split every version into provisions, compare consecutive versions, and credit each change to the enactment
the table names for that version's day. A change the table cannot separate is labelled and credited to none.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')
import pymupdf  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = HERE / '.cache'
BASE = 'https://www.gibraltarlaws.gov.gi'
UA = 'lexifina-watch/1.0 (+https://lexifina.com/watch; gibraltar-law@lexifina.com)'
PAUSE = 5.0          # robots.txt: "User-agent: * / Crawl-delay: 5"; requests are therefore serial
COMMITTER = ('Lexifina', 'gibraltar-law@lexifina.com')
PUBLISHER = ('Gibraltar Law Offices (gibraltarlaws.gov.gi)', 'gibraltarlaws@gibraltarlaws.invalid')

ACTS = [
    {'slug': 'constitution', 'kind': 'order', 'id': '2007-00', 'short': 'Gibraltar Constitution Order 2006',
     'page': '/legislations/gibraltar-constitution-order-2006-1834', 'made': '2006-12-14',
     'author': ('Gibraltar Constitution Order 2006', 'order-2006-constitution@gibraltarlaws.invalid'),
     'tag': 'order/2006-constitution'},
    {'slug': 'stamp-duties', 'kind': 'act', 'id': '2005-73', 'short': 'Stamp Duties Act 2005',
     'page': '/legislations/stamp-duties-act-2005-1262', 'author': ('Act 2005-73', 'act-2005-73@gibraltarlaws.invalid'),
     'tag': 'act/2005-73'},
]

# ---------------------------------------------------------------- fetching

REQUESTS: list[dict] = []
_lock = threading.Lock()
_last = [0.0]
NOT_FOUND = b'\x00not-found\x00'


def _get(url: str) -> bytes:
    with _lock:
        wait = _last[0] + PAUSE - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return NOT_FOUND
        raise
    except Exception as exc:   # a certificate chain Python rejects on some machines: fall back to curl
        if 'CERTIFICATE' not in str(exc).upper():
            raise
        out = subprocess.run(['curl', '-sS', '-L', '--max-redirs', '4', '-A', UA, '-w', '%{http_code}', url], capture_output=True)
        if out.returncode:
            raise RuntimeError(f'curl {url}: {out.stderr.decode(errors="replace")}')
        body, code = out.stdout[:-3], out.stdout[-3:]
        return NOT_FOUND if code == b'404' else body


def cache_path(url: str) -> Path:
    return CACHE / hashlib.sha256(url.encode()).hexdigest()[:32]


def fetch(url: str, offline: bool = False, allow_missing: bool = False) -> bytes:
    """GET with a file cache keyed by the URL (404s are cached too), so a rebuild reads the same bytes."""
    path = cache_path(url)
    with _lock:
        REQUESTS.append({'url': url, 'file': path})
    if not path.exists():
        if offline:
            raise SystemExit(f'not cached: {url}')
        CACHE.mkdir(parents=True, exist_ok=True)
        (CACHE / '.gitignore').write_text('*\n')
        for attempt in range(4):
            try:
                body = _get(url)
                if body != NOT_FOUND:
                    if url.endswith('.pdf') and not body.startswith(b'%PDF'):
                        raise RuntimeError(f'not a PDF: {url}')
                    if not url.endswith('.pdf') and b'gibraltarlaws' not in body:
                        raise RuntimeError(f'unexpected page: {url}')
                path.write_bytes(body)
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(5 * (attempt + 1))
    body = path.read_bytes()
    if body == NOT_FOUND:
        if allow_missing:
            return b''
        raise SystemExit(f'404: {url}')
    return body


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- the act page

MONTHS = {m: i + 1 for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                          'September', 'October', 'November', 'December'])}


def text_of_html(h: str) -> str:
    h = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', ' ', h, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))


def iso(dmy: str) -> str:
    d, m, y = dmy.split('-')
    return f'{y}-{m}-{d}'


def act_page(act: dict, offline: bool) -> dict:
    """The act's page: title, its dated versions (each with the PDF of that version), and the amending legislation."""
    url = BASE + act['page']
    html = fetch(url, offline).decode('utf-8', 'replace')
    title = re.search(r'<title>\s*(.*?)\s*[|<]', html, re.S)
    pdfs = sorted(set(re.findall(r'uploads/legislations/[^"\'\s]+\.pdf', html)))
    days = sorted(set(re.findall(r'/version/(\d\d-\d\d-\d{4})', html)), key=iso)
    versions = []
    for d in days:
        yy = d[-2:]
        want = f'({d[:2]}-{d[3:5]}-{yy}).pdf'
        match = [p for p in pdfs if p.endswith(want)]
        if not match and len(days) == 1:
            match = [p for p in pdfs if re.fullmatch(r'.*/\d{4}-\d+\.pdf', p)]
        if not match and d == days[0]:
            match = [p for p in pdfs if p.endswith('o.pdf')]   # the first version is the act as enacted
        if len(match) != 1:
            raise SystemExit(f'{act["slug"]} {d}: PDF for the version not found: {match}')
        versions.append({'from': iso(d), 'pdf': f'{BASE}/{match[0]}', 'page': f'{url}/version/{d}'})
    amend = []
    i = html.find('id="connected-legislation"')
    block = html[i:i + 60000] if i >= 0 else ''
    for tr in re.findall(r'<div class="tr">(.*?)</div>\s*</div>\s*(?=<div class="tr">|</div>)', block, re.S):
        cells = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', c)).strip() for c in re.findall(r'<p>(.*?)</p>', tr, re.S)]
        link = re.search(r'href="([^"]*legislations/[^"]*)"', tr)
        if len(cells) >= 3 and link:
            amend.append({'number': cells[0], 'title': cells[1], 'type': cells[2], 'date': cells[3] if len(cells) > 3 else '',
                          'url': link.group(1)})
    return {'url': url, 'html': html, 'title': act['short'], 'versions': versions, 'amending': amend,
            'sha256': sha(html.encode())}


def amending_meta(a: dict, offline: bool) -> dict:
    """An amending act: its page, its PDF, the day it was assented to and the Gazette issue, read from the PDF."""
    out = {'number': a['number'], 'title': a['title'], 'type': a['type'], 'url': a['url'], 'assent': None,
           'gazette': None, 'pdf': None}
    html = fetch(a['url'], offline, allow_missing=True).decode('utf-8', 'replace')
    pdfs = re.findall(r'uploads/legislations/[^"\'\s]+\.pdf', html)
    if not pdfs:
        return out
    out['pdf'] = f'{BASE}/{pdfs[0]}'
    raw = fetch(out['pdf'], offline, allow_missing=True)
    if not raw:
        return out
    doc = pymupdf.open(stream=raw, filetype='pdf')
    first = ' '.join(re.sub(r'\s+', ' ', doc[i].get_text()) for i in range(min(2, doc.page_count)))
    out['sha256'] = sha(raw)
    pat = r'(\d{1,2})(?:st|nd|rd|th)?\s+(%s)\s+(\d{4})' % '|'.join(MONTHS)
    m = re.search(r'I\s+ASSENT.{0,200}?' + pat, first, re.S | re.I) or re.search(r'ASSENT.{0,200}?' + pat, first, re.S)
    if m:
        out['assent'] = f'{int(m.group(3)):04d}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}'
    g = re.search(r'GAZETTE.{0,80}?No\.\s*(\d+)\s+GIBRALTAR\s+\w+day\s+' + pat, first, re.S | re.I)
    if g:
        out['gazette'] = {'no': g.group(1), 'date': f'{int(g.group(4)):04d}-{MONTHS[g.group(3)]:02d}-{int(g.group(2)):02d}'}
    return out


# ---------------------------------------------------------------- reading one PDF

HF = re.compile(r'^(Stamp Duties|\d{4}-\d+|This version is out of date|© Government of Gibraltar.*|Page \d+ of \d+|\d{1,3})$')
RULE = re.compile(r'_{5,}')
PRIVATE = {'': '–', ' ': ' ', ' ': ' ', '​': ''}
WS = re.compile(r'\s+')


def norm(s: str) -> str:
    """Runs of white space become one space; the private-use minus glyph the publisher's font uses for a dash becomes
    an en dash (what the same PDFs print elsewhere for a dash). Nothing else changes."""
    for a, b in PRIVATE.items():
        s = s.replace(a, b)
    return WS.sub(' ', s).strip()


def line_text(chars: list[dict]) -> str:
    raw = ''.join(c['c'] for c in chars)
    toks = raw.split(' ')
    if len(toks) >= 8 and sum(len(t) == 1 for t in toks) / len(toks) > 0.8:
        # letter-spaced line: a space glyph after every letter; keep a space only where the glyphs show a gap
        out, prev = [], None
        for c in chars:
            if c['c'] == ' ':
                continue
            if prev is not None and c['bbox'][0] - prev['bbox'][2] > 0.5:
                out.append(' ')
            out.append(c['c'])
            prev = c
        raw = ''.join(out)
    return norm(raw)


class Line:
    __slots__ = ('page', 'x0', 'y0', 'text', 'bold')

    def __init__(self, page, x0, y0, text, bold):
        self.page, self.x0, self.y0, self.text, self.bold = page, x0, y0, text, bold


def page_lines(doc) -> tuple[list[Line], list[str]]:
    """Every line of the pages, in the PDF's own order, without the running header and footer. The publisher changed
    its page template three times, so a header or footer line is recognised by what it says, in the top or bottom of the
    page; blank lines in the footer are dropped, blank lines in the text are kept (they separate paragraphs)."""
    body: list[Line] = []
    problems: list[str] = []
    for pno, page in enumerate(doc):
        h = page.rect.height
        for b in page.get_text('rawdict')['blocks']:
            if b['type']:
                continue
            for l in b['lines']:
                spans = l['spans']
                chars = [c for s in spans for c in s['chars']]
                text = line_text(chars)
                x0, y0 = l['bbox'][0], l['bbox'][1]
                top, bottom = y0 < 0.14 * h, y0 > 0.88 * h
                if RULE.fullmatch(text):
                    continue
                if (top or bottom) and (HF.match(text) or (bottom and not text)):
                    continue
                if y0 > 0.94 * h and text:
                    problems.append(f'unrecognised text in the footer zone, page {pno + 1}: {text[:40]!r}')
                bold = bool(text) and all('Bold' in s['font'] for s in spans if ''.join(c['c'] for c in s['chars']).strip())
                body.append(Line(pno, x0, y0, text, bold))
    return body, problems


class Para:
    __slots__ = ('lines', 'x0', 'page')

    def __init__(self, lines):
        self.lines = lines
        self.x0 = lines[0].x0
        self.page = lines[0].page

    @property
    def text(self) -> str:
        return ' '.join(l.text for l in self.lines)

    @property
    def heading_like(self) -> bool:
        margin = MARGIN[0]
        return all(l.bold or (l.text.isupper() and l.x0 > margin + 25) or (len(l.text) < 120 and l.text in ARR[0])
                   for l in self.lines)


MARGIN = [0.0]
ARR = ['']   # the text of the arrangement of sections: marginal notes and part headings are named there


HEAD_START = re.compile(r'^(SCHEDULE( \d+)?( TO THE CONSTITUTION)?|ANNEX \d TO THE ORDER)$')


ENUM = re.compile(r'^(\(\w{1,5}\)\s|“|Provided that)')
END = re.compile(r'(?:[;.:,–—]|(?:and|or))$')


def paragraphs(lines: list[Line]) -> list[Para]:
    """A paragraph is a run of non-blank lines: the PDF puts a whitespace-only line between paragraphs. A run that
    crosses a page break continues (the page's own leading blank line is not a break)."""
    out: list[Para] = []
    cur: list[Line] = []
    for l in lines:
        if not l.text:
            if cur and cur[-1].page == l.page:
                out.append(Para(cur))
                cur = []
            continue
        if cur and (HEAD_START.match(l.text) or l.page != cur[-1].page and (l.bold or (len(l.text) < 120 and l.text in ARR[0]))):
            out.append(Para(cur))   # a heading at the top of a page starts a paragraph
            cur = []
        elif cur and SEC.match(l.text) and abs(l.x0 - MARGIN[0]) <= 2:
            # a marginal note (bold, or named in the arrangement of sections) directly above its section
            k = len(cur)
            while k > 0 and (cur[k - 1].bold or (len(cur[k - 1].text) < 120 and cur[k - 1].text in ARR[0])) and k > len(cur) - 3:
                k -= 1
            if k < len(cur):
                if k > 0:
                    out.append(Para(cur[:k]))
                cur = cur[k:]
                if not (l.bold and False):
                    out.append(Para(cur))
                    cur = []
        if cur and ENUM.match(l.text) and END.search(cur[-1].text):
            out.append(Para(cur))   # the PDF sometimes leaves out the blank line between two paragraphs
            cur = []
        cur.append(l)
        if HEAD_START.match(l.text):
            out.append(Para(cur))
            cur = []
    if cur:
        out.append(Para(cur))
    return out


LISTITEM = re.compile(r'(?<=;)\s+(?=(?:(?:and|or)\s+)?\([a-z]{1,4}\)\s)|(?<=;\sand)\s+(?=\([a-z]{1,4}\)\s)|(?<=;\sor)\s+(?=\([a-z]{1,4}\)\s)')


def split_text(t: str) -> list[str]:
    """A list item that follows another on the same printed line is a paragraph of its own."""
    return [x for x in LISTITEM.split(t) if x]


def join_connectives(paras: list[str]) -> list[str]:
    """A line with only 'and' or 'or' between two list items belongs to the item before it (other layouts print '; and')."""
    out: list[str] = []
    for p in paras:
        if out and re.fullmatch(r'(?:and|or)', p):
            out[-1] += ' ' + p
        else:
            out.append(p)
    return out


def merge_rows(lines: list[Line]) -> list[str]:
    """Visual rows: lines on the same page whose tops are within 3 points, left to right."""
    rows: list[list[Line]] = []
    for l in lines:
        if not l.text:
            continue
        if rows and rows[-1][0].page == l.page and abs(rows[-1][0].y0 - l.y0) <= 3:
            rows[-1].append(l)
        else:
            rows.append([l])
    return [' '.join(x.text for x in sorted(r, key=lambda x: x.x0)) for r in rows]


SEC = re.compile(r'^(\d+)([A-Z]{0,2})\.(?=[\s(\-]|$)')


def sec_key(m) -> tuple[int, str]:
    return int(m.group(1)), m.group(2)


def read_version(raw: bytes, kind: str) -> dict:
    """One PDF as units (provisions in document order, with the headings that open them), its table of amending
    enactments (acts only), and the problems found."""
    doc = pymupdf.open(stream=raw, filetype='pdf')
    body, problems = page_lines(doc)
    a0 = None
    for n, l in enumerate(body):
        if l.text.startswith('ARRANGEMENT OF SECTIONS') if kind == 'act' else l.text.startswith('ANNEX 1 TO THE ORDER'):
            a0 = n
            break
    front = body[:a0] if kind == 'act' and a0 is not None else []
    rest = body[a0:] if kind == 'act' else body
    xs: dict[int, int] = {}
    for l in rest:
        if len(l.text) > 30:
            xs[round(l.x0)] = xs.get(round(l.x0), 0) + 1
    MARGIN[0] = float(max(xs, key=xs.get))
    units: dict[str, dict] = {}
    table: list[dict] = []
    notes: dict[str, str] = {}

    def put(key: str, label: str, paras: list[str]):
        units[key] = {'key': key, 'label': label, 'text': '\n\n'.join(paras) + '\n'}

    if kind == 'act':
        i = next((i for i, l in enumerate(front) if l.text.startswith('Amending')), len(front))
        head = merge_rows([l for l in front[:i]])
        put('front', 'Title and commencement of the act', head)
        cells = [l for l in front[i:] if l.text]
        row = None
        m0 = MARGIN[0]
        for c in cells:
            t = c.text
            if c.x0 < m0 + 81 and re.fullmatch(r'(?:Act\.?\s*)?\d{4}-\d+', t):
                row = {'law': re.search(r'\d{4}-\d+', t).group(0), 'provisions': '', 'date': None, 'note': None}
                table.append(row)
            elif row is not None and c.x0 >= m0 + 81 and row['date'] is None and re.search(r'(?:^|\s)\d{1,2}\.\d{1,2}\.\d{4}\d?$', t):
                mm = re.match(r'^(.*?)\s*(\d{1,2})\.(\d{1,2})\.(\d{4})(\d?)$', t)
                if mm.group(1):
                    row['provisions'] = (row['provisions'] + ' ' + mm.group(1)).strip()
                row['date'] = f'{mm.group(4)}-{int(mm.group(3)):02d}-{int(mm.group(2)):02d}'
                row['note'] = mm.group(5) or None
            elif row is not None and m0 + 81 <= c.x0 < m0 + 321 and row['date'] is None:
                row['provisions'] = (row['provisions'] + ' ' + t).strip()
            elif re.match(r'^\d ', t) and row is not None and row['date'] is not None:
                notes[t[0]] = t[2:].strip()
        for r in table:
            r['note'] = notes.get(r['note']) if r['note'] else None
            if r['date'] is None:
                problems.append(f'table row without date: {r}')

    # the arrangement of sections is a table of contents: one visual row per line; the rest is paragraphs
    a1 = None
    if a0 is not None:
        for n in range(a0 + 1, len(body)):
            l = body[n]
            if (kind == 'act' and l.text.startswith('AN ACT')) or (kind == 'order' and l.bold and l.text.startswith('CHAPTER')):
                a1 = n
                break
    ARR[0] = ' ' + ' '.join(l.text for l in body[a0:a1]) + ' ' if a0 is not None and a1 is not None else ''
    items: list = []
    if a0 is not None:
        if a1 is None:
            raise SystemExit('end of the arrangement of sections not found')
        items = (paragraphs(body[:a0]) if kind == 'order' else []) + [('arrangement', merge_rows(body[a0:a1]))] + paragraphs(body[a1:])
    else:
        items = paragraphs(body)

    prefix = 'order/' if kind == 'order' else ''
    expect = [0, '']
    cur: dict | None = None
    order: list[dict] = []
    in_schedule = [False]

    def start(key: str, label: str, paras: list[Para] | list[str]) -> dict:
        nonlocal cur
        cur = {'key': key, 'label': label, 'paras': list(paras)}
        order.append(cur)
        return cur

    for it in items:
        if isinstance(it, tuple):
            key = 'annex1/arrangement' if kind == 'order' else 'arrangement'
            cur = None
            order.append({'key': key, 'label': 'Arrangement of sections', 'rows': it[1]})
            prefix = 'annex1/' if kind == 'order' else ''
            expect[:] = [0, '']
            in_schedule[0] = False
            continue
        p: Para = it
        text = p.text
        m = re.match(r'^ANNEX (\d) TO THE ORDER', text) if kind == 'order' else None
        sch = re.match(r'^SCHEDULE(?: (\d+))?(?: TO THE CONSTITUTION)?$', text) if p.heading_like else None
        sm = SEC.match(text) if abs(p.x0 - MARGIN[0]) <= 2 and not in_schedule[0] else None
        if m:
            prefix = f'annex{m.group(1)}/'
            expect[:] = [0, '']
            in_schedule[0] = False
            start(prefix + 'head', f'Annex {m.group(1)}', [p])
        elif sch:
            in_schedule[0] = True
            n = sch.group(1)
            start(prefix + (f'sch-{n}' if n else 'schedule'), f'Schedule {n}' if n else 'Schedule', [p])
        elif sm and ((sec_key(sm)[0] == expect[0] + 1 and not sec_key(sm)[1]) or (sec_key(sm)[0] == expect[0] and sec_key(sm)[1] > expect[1] and expect[0] > 0)):
            n, suf = sec_key(sm)
            expect[:] = [n, suf]
            pulled: list[Para] = []
            if cur is not None and 'paras' in cur:
                while cur['paras'] and cur['paras'][-1].heading_like and len(cur['paras']) > (0 if cur['key'].endswith(('head', 'preamble', 'intro')) else 1):
                    pulled.insert(0, cur['paras'].pop())
            start(f'{prefix}s-{n:03d}{suf}', f's. {n}{suf}', pulled + [p])
        else:
            if sm and not in_schedule[0]:
                problems.append(f'numbered paragraph out of sequence after {expect}: {text[:50]!r}')
            if cur is None or 'paras' not in cur:
                start(prefix + ('intro' if kind == 'act' else 'preamble'), 'Opening words', [])
            cur['paras'].append(p)
    for u in order:
        if 'rows' in u:
            put(u['key'], u['label'], u['rows'])
        elif u['paras']:
            put(u['key'], u['label'], join_connectives([t for p in u['paras'] for t in split_text(p.text)]))
    return {'units': units, 'table': table, 'problems': problems, 'pages': doc.page_count}


def official_words(raw: bytes, kind: str) -> list[str]:
    """All the words of the PDF, read without the parser above: PyMuPDF's word list in its own order, without the
    running header and footer and (for acts) the table of amending enactments on page 1."""
    doc = pymupdf.open(stream=raw, filetype='pdf')
    out: list[str] = []
    for page in doc:
        h = page.rect.height
        lines: dict[tuple, list] = {}
        for w in page.get_text('words'):
            lines.setdefault((w[5], w[6]), []).append(w)
        for ws in lines.values():
            text = norm(' '.join(w[4] for w in ws))
            y0 = ws[0][1]
            if RULE.fullmatch(text):
                continue
            if (y0 < 0.14 * h or y0 > 0.88 * h) and HF.match(text):
                continue
            out.extend(t for w in ws for t in norm(w[4]).split(' ') if t)
    if kind == 'act' and 'Amending' in out:
        i = out.index('Amending')
        j = next(n for n in range(i, len(out)) if out[n:n + 3] == ['ARRANGEMENT', 'OF', 'SECTIONS'])
        del out[i:j]
    return out


# ---------------------------------------------------------------- provisions named in the table

def label_of(key: str) -> str:
    base = key.rsplit('/', 1)[-1]
    m = re.fullmatch(r's-(\d+)([A-Z]*)', base)
    if m:
        return f's. {int(m.group(1))}{m.group(2)}'
    m = re.fullmatch(r'sch-(\d+)', base)
    if m:
        return f'Sch. {m.group(1)}'
    return {'front': 'Title and commencement', 'arrangement': 'Arrangement of sections', 'intro': 'Long title',
            'schedule': 'Schedule', 'preamble': 'Opening words', 'head': 'Annex heading'}.get(base, base) \
        + (f' ({key.split("/")[0]})' if '/' in key else '')


def sec_sort(key: str) -> tuple:
    base = key.rsplit('/', 1)[-1]
    m = re.fullmatch(r's-(\d+)([A-Z]*)', base)
    return (int(m.group(1)), m.group(2)) if m else (9999, base)


def provisions_named(text: str, unit_keys: list[str]) -> set[str]:
    """'ss. 2, 4, 4A-4B, 46(j)-(k), Sch. 1' -> the unit keys they name (a section's subsections count as the section)."""
    secs = sorted((k for k in unit_keys if re.fullmatch(r's-\d+[A-Z]*', k)), key=sec_sort)
    out: set[str] = set()
    depth, tok, toks = 0, '', []
    for ch in text:
        depth += (ch == '(') - (ch == ')')
        if ch == ',' and depth == 0:
            toks.append(tok)
            tok = ''
        else:
            tok += ch
    toks.append(tok)
    toks = [x for t in toks for x in re.split(r'\s+(?:and|&)\s+', t)]
    for t in toks:
        t = t.strip()
        t = re.sub(r'^(?:ss?|Schs?)\.\s*', lambda m: 'SCH ' if m.group(0).startswith('S') and 'ch' in m.group(0) else '', t)
        if t.startswith('('):
            continue
        if t.startswith('SCH '):
            out.add(f'sch-{re.match(r"\d+", t[4:]).group(0)}') if re.match(r'\d+', t[4:]) else None
            continue
        r = re.fullmatch(r'(\d+[A-Z]*)\s*-\s*(\d+[A-Z]*)', t)
        if r:
            lo, hi = f's-{int(re.match(chr(92) + "d+", r.group(1)).group(0)):03d}{r.group(1).lstrip("0123456789")}', \
                f's-{int(re.match(chr(92) + "d+", r.group(2)).group(0)):03d}{r.group(2).lstrip("0123456789")}'
            out.update(k for k in secs if sec_sort(lo) <= sec_sort(k) <= sec_sort(hi))
            continue
        m = re.match(r'(\d+)([A-Z]*)', t)
        if m:
            out.add(f's-{int(m.group(1)):03d}{m.group(2)}')
    return out


# ---------------------------------------------------------------- one act: versions, changes, causes

def build_act(act: dict, offline: bool) -> dict:
    page = act_page(act, offline)
    versions = []
    for v in page['versions']:
        raw = fetch(v['pdf'], offline)
        r = read_version(raw, act['kind'])
        versions.append({**v, 'units': r['units'], 'table': r['table'], 'problems': r['problems'], 'sha256': sha(raw),
                         'pages': r['pages']})
    if not versions:
        raise SystemExit(f'{act["slug"]}: no versions')
    problems: list[str] = []
    for v in versions:
        problems += [f'{v["from"]}: {p}' for p in v['problems']]
    versions.sort(key=lambda v: v['from'])
    laws: dict[str, dict] = {}
    table: list[dict] = []
    if act['kind'] == 'act':
        # Older PDFs drop rows for provisions since replaced: the record is the union, the newest wording first.
        for v in reversed(versions):
            for r in v['table']:
                if not any(t['law'] == r['law'] and t['date'] == r['date'] for t in table):
                    table.append(r)
        table.sort(key=lambda r: r['date'])
        titles = {a['number']: a for a in page['amending']}
        for r in table:
            if r['law'] not in laws:
                a = titles.get(r['law'])
                if a is None:
                    raise SystemExit(f'amending enactment {r["law"]} is not listed on the act page')
                laws[r['law']] = amending_meta(a, offline)
        for v in versions[1:]:
            own = [r for r in v['table'] if r['date'] == v['from']]
            if not own:
                problems.append(f'{v["from"]}: its own table has no row for this day')
        by_date: dict[str, set[str]] = {}
        for v in versions:
            for r in v['table']:
                by_date.setdefault(r['date'], set()).add(r['law'])
        problems += [f'tables disagree on the enactment of {d}: {sorted(l)}' for d, l in by_date.items() if len(l) > 1]
    changes = []
    for prev, cur in zip(versions, versions[1:]):
        keys = list(dict.fromkeys(list(prev['units']) + list(cur['units'])))
        changed = [k for k in keys if (prev['units'].get(k) or {}).get('text') != (cur['units'].get(k) or {}).get('text')]
        rows = [r for r in cur['table'] if r['date'] == cur['from']] or [r for r in table if r['date'] == cur['from']]
        lawsd = list(dict.fromkeys(r['law'] for r in rows))
        derived = {k for k in changed if k.rsplit('/', 1)[-1] in ('front', 'arrangement', 'intro')}
        real = [k for k in changed if k not in derived]
        named: dict[str, set[str]] = {}
        for l in lawsd:
            ks: set[str] = set()
            for r in rows:
                if r['law'] == l:
                    ks |= provisions_named(r['provisions'], list(cur['units']))
            named[l] = ks
        groups: dict[str, list[str]] = {}
        why: dict[str, str] = {}
        for k in real:
            cov = [l for l in lawsd if k in named[l]]
            if len(lawsd) == 1:
                groups.setdefault(lawsd[0], []).append(k)
                why[k] = 'commencement table: law and provision named' if cov else 'commencement table: date only (provision not named)'
            elif len(cov) == 1:
                groups.setdefault(cov[0], []).append(k)
                why[k] = 'commencement table: law and provision named'
            elif len(lawsd) > 1:
                groups.setdefault('candidates', []).append(k)
                why[k] = 'several enactments took effect that day'
            else:
                groups.setdefault('unexplained', []).append(k)
                why[k] = 'the commencement table names no enactment for this day'
        credited = [g for g in groups if g not in ('candidates', 'unexplained')]
        for k in sorted(derived):
            if not lawsd:
                g = 'unexplained'
            elif len(lawsd) == 1:
                g = lawsd[0]
            elif len(credited) == 1 and 'candidates' not in groups:
                g = credited[0]
            else:
                g = 'candidates'
            groups.setdefault(g, []).append(k)
            why[k] = 'follows the provisions changed that day'
        for l in lawsd:
            groups.setdefault(l, [])
        changes.append({'from': cur['from'], 'prev': prev, 'cur': cur, 'laws': lawsd, 'rows': rows, 'groups': groups,
                        'why': why, 'changed': changed})
    for r in table:
        if r['date'] not in {v['from'] for v in versions}:
            problems.append(f'table row {r["law"]} {r["date"]} has no version of that day')
    return {'act': act, 'page': page, 'versions': versions, 'changes': changes, 'laws': laws, 'table': table,
            'problems': problems}


# ---------------------------------------------------------------- git

def git(repo: Path, *args: str, env: dict | None = None, input: str | None = None) -> str:
    out = subprocess.run(['git', *args], cwd=repo, capture_output=True, text=True, encoding='utf-8', env=env, input=input)
    if out.returncode:
        raise SystemExit(f'git {" ".join(args)} failed: {out.stderr}')
    return out.stdout


def last_sunday(year: int, month: int) -> dt.date:
    d = (dt.date(year, month + 1, 1) if month < 12 else dt.date(year + 1, 1, 1)) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def gibraltar_offset(day: dt.date) -> int:
    """Hours ahead of UTC at noon in Gibraltar (written out: this machine has no tz database). Central European Time,
    summer time from the last Sunday in March to the last Sunday in October (start <= day < end)."""
    y = day.year
    return 2 if last_sunday(y, 3) <= day < last_sunday(y, 10) else 1


def commit_date(day: str, seq: list[int]) -> str:
    d = dt.date.fromisoformat(day)
    if d.year < 1970:
        seq[0] += 1
        return f'@{seq[0]} +0000'
    off = gibraltar_offset(d)
    stamp = int(dt.datetime(d.year, d.month, d.day, 12, tzinfo=dt.timezone(dt.timedelta(hours=off))).timestamp())
    return f'@{stamp} +0{off}00'


def file_of(key: str) -> str:
    return key + '.md'


def write_unit(repo: Path, slug: str, key: str, unit: dict | None):
    path = repo / slug / file_of(key)
    if unit is None:
        path.unlink(missing_ok=True)
        if path.parent != repo / slug and path.parent.exists() and not any(path.parent.iterdir()):
            path.parent.rmdir()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(unit['text'], encoding='utf-8', newline='\n')


def labels(units: dict, keys: list[str], prev: dict) -> list[str]:
    out = []
    for k in keys:
        was, now = k in prev, k in units
        word = 'inserted' if now and not was else 'removed' if was and not now else 'amended'
        out.append(f'{label_of(k)} ({word})')
    return out


def plan_commits(built: list[dict]) -> list[tuple]:
    commits = []
    for ai, b in enumerate(built):
        commits.append((b['versions'][0]['from'], ai, 0, '', {'kind': 'start', 'b': b}))
        for ch in b['changes']:
            for g in ch['groups']:
                if g not in ('candidates', 'unexplained'):
                    commits.append((ch['from'], ai, 1, g, {'kind': 'law', 'b': b, 'ch': ch, 'law': g}))
            if 'candidates' in ch['groups']:
                commits.append((ch['from'], ai, 2, '', {'kind': 'candidates', 'b': b, 'ch': ch}))
            if 'unexplained' in ch['groups']:
                commits.append((ch['from'], ai, 3, '', {'kind': 'unexplained', 'b': b, 'ch': ch}))
    commits.sort(key=lambda c: c[:4])
    return commits


def start_message(b: dict, day: str):
    act = b['act']
    v = b['versions'][0]
    if act['kind'] == 'order':
        msg = [f'{act["short"]}: the Constitution of Gibraltar as in force from {day}', '',
               'The Order in Council as the Gibraltar Laws site publishes it: the Order, Annex 1 (the Constitution),',
               'its Schedule and Annex 2 (transitional provisions). The site holds one version; no later version exists',
               'there, so no later amendment is applied.', '']
        trailers = ['Kind: Order in Council', f'Made: {act["made"]}', f'In-force: {day}',
                    'Evidence: the site dates its one version 02-01-2007',
                    f'Source: {b["page"]["url"]}', f'Consolidated: {v["page"]}', f'PDF: {v["pdf"]}']
        return act['author'], msg, trailers
    key = act['id']
    front = v['units']['front']['text'].replace('\n\n', ' ')
    assent = re.search(r'Assent (\d+)\.(\d+)\.(\d{4})', front)
    comm = re.search(r'Commencement \((LN\.[\d/]+)\)', front)
    msg = [f'{act["short"]} ({key}), in force from {day}', '',
           'The act in the first dated version the Gibraltar Laws site publishes. Its table of amending enactments is',
           'empty for this version: it is the act as enacted and commenced.', '']
    trailers = ['Kind: Act']
    if assent:
        trailers.append(f'Enacted: {int(assent.group(3)):04d}-{int(assent.group(2)):02d}-{int(assent.group(1)):02d}')
    if comm:
        trailers.append(f'Commencement-notice: {comm.group(1)}')
    trailers += [f'In-force: {day}', f'Source: {b["page"]["url"]}', f'Consolidated: {v["page"]}', f'PDF: {v["pdf"]}']
    return act['author'], msg, trailers


def change_message(b: dict, ch: dict, kind_: str, law: str | None, day: str):
    act = b['act']
    keys = ch['groups'].get(law if kind_ == 'law' else kind_, [])
    ls = labels(ch['cur']['units'], keys, ch['prev']['units'])
    cur = ch['cur']
    trailers = []
    if kind_ == 'law':
        lm = b['laws'][law]
        rows = [r for r in ch['rows'] if r['law'] == law]
        if keys and len(keys) <= 6:
            subj = ', '.join(label_of(k) for k in keys)
        else:
            subj = f'{len(keys)} provisions' if keys else 'no words of the act'
        msg = [f'{act["short"]}: {subj} (Act {law})', '', f'{lm["title"]} (Act {law}) took effect for this act on {day}.']
        if keys:
            msg += ['', 'Changed: ' + '; '.join(ls) + '.']
        else:
            msg += ['', 'No word of the act changed that day; the table lists the enactment for this day.']
        msg += ['']
        author = (f'Act {law}', f'act-{law}@gibraltarlaws.invalid')
        trailers += [f'Kind: {lm["type"]}']
        if lm.get('assent'):
            trailers.append(f'Enacted: {lm["assent"]}')
        if lm.get('gazette'):
            trailers.append(f'Published: {lm["gazette"]["date"]} (Gibraltar Gazette No. {lm["gazette"]["no"]})')
        trailers += [f'In-force: {day}', f'Affecting: {act["short"]}', 'Provisions: ' + '; '.join(r['provisions'] for r in rows)]
        notyet = [label_of(k) for k in keys if 'date only' in ch['why'].get(k, '')]
        trailers.append('Evidence: commencement table of the act (enactment, provisions, day)' +
                        (f'; date only for {", ".join(notyet)}' if notyet else ''))
        for r in rows:
            if r.get('note'):
                trailers.append(f'Commencement-notice: {r["note"]}')
        trailers += [f'Source: {lm["url"]}', f'Consolidated: {cur["page"]}', f'PDF: {cur["pdf"]}']
        return author, msg, trailers, keys
    if kind_ == 'candidates':
        msg = [f'{act["short"]}: {len(keys)} provisions changed the day several enactments took effect', '',
               'Changed: ' + '; '.join(ls) + '.', '',
               f'Several enactments took effect on {day} and the commencement table does not say which provision each',
               'changed. The change is credited to none of them.', '']
        trailers += [f'In-force: {day}', f'Affecting: {act["short"]}', 'Evidence: none sufficient to separate the enactments']
        trailers += [f'Candidate: Act {l}' for l in ch['laws']]
    else:
        msg = [f'{act["short"]}: {len(keys)} provisions changed with no enactment named', '',
               'Changed: ' + '; '.join(ls) + '.', '',
               f'The commencement table names no enactment for {day}, the day of this version. Credited to no law.', '']
        trailers += [f'In-force: {day}', f'Affecting: {act["short"]}', 'Evidence: none']
    trailers += [f'Consolidated: {cur["page"]}', f'PDF: {cur["pdf"]}']
    return PUBLISHER, msg, trailers, keys


def write_repo(repo: Path, built: list[dict], docs: Path, today: str):
    remote = None
    if (repo / '.git').exists():
        out = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=repo, capture_output=True, text=True)
        remote = out.stdout.strip() or None

    def force(fn, path, _exc):
        os.chmod(path, 0o700)
        fn(path)
    if repo.exists():
        for p in repo.iterdir():
            if p.is_dir():
                shutil.rmtree(p, onexc=force)
            else:
                os.chmod(p, 0o700)
                p.unlink()
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, 'init', '-q', '-b', 'main')
    git(repo, 'config', 'core.autocrlf', 'false')
    if remote:
        git(repo, 'remote', 'add', 'origin', remote)
    seq = [0]
    tags: dict[str, str] = {}
    law_days: dict[str, list[tuple[str, str]]] = {}
    log = []
    for day, ai, _, _, c in plan_commits(built):
        b = c['b']
        slug = b['act']['slug']
        if c['kind'] == 'start':
            for key, u in b['versions'][0]['units'].items():
                write_unit(repo, slug, key, u)
            author, msg, trailers = start_message(b, day)
            keys = list(b['versions'][0]['units'])
            law = b['act']['tag']
        else:
            law = c.get('law')
            author, msg, trailers, keys = change_message(b, c['ch'], c['kind'], law, day)
            for k in keys:
                write_unit(repo, slug, k, c['ch']['cur']['units'].get(k))
        git(repo, 'add', '-A')
        when = commit_date(day, seq)
        env = {**os.environ, 'GIT_AUTHOR_NAME': author[0], 'GIT_AUTHOR_EMAIL': author[1], 'GIT_AUTHOR_DATE': when,
               'GIT_COMMITTER_NAME': COMMITTER[0], 'GIT_COMMITTER_EMAIL': COMMITTER[1], 'GIT_COMMITTER_DATE': when}
        git(repo, 'commit', '-q', '--allow-empty', '--cleanup=verbatim', '-F', '-', env=env,
            input='\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n')
        head = git(repo, 'rev-parse', 'HEAD').strip()
        tags[f'{slug}/{day}'] = head
        if c['kind'] in ('law', 'start'):
            law_days.setdefault(law, []).append((day, head))
        log.append({'day': day, 'slug': slug, 'kind': c['kind'], 'law': law, 'author': author[0], 'units': len(keys),
                    'clamped': day < '1970-01-01', 'keys': keys})
    for law, days in law_days.items():
        pref = law if '/' in law else f'act/{law}'
        if len(days) == 1:
            tags[pref] = days[0][1]
        else:
            for day, head in days:
                tags[f'{pref}/{day}'] = head
    for name, head in tags.items():
        git(repo, 'tag', '-f', name, head)
    for p in sorted(docs.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            dest = repo / p.relative_to(docs)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(p.read_bytes())
    for name in ('build.py', 'reproduce.py', 'check_repo.py', 'test_repo.py'):
        (repo / 'tools' / name).write_bytes((HERE / name).read_bytes())
    write_tables(repo, built)
    from reproduce import write_manifest, write_reproduce
    write_manifest(repo, built, today, log)
    write_reproduce(repo, built, log, tags, REQUESTS, today)
    git(repo, 'add', '-A')
    when = commit_date(today, seq)
    env = {**os.environ, 'GIT_AUTHOR_NAME': COMMITTER[0], 'GIT_AUTHOR_EMAIL': COMMITTER[1], 'GIT_AUTHOR_DATE': when,
           'GIT_COMMITTER_NAME': COMMITTER[0], 'GIT_COMMITTER_EMAIL': COMMITTER[1], 'GIT_COMMITTER_DATE': when}
    git(repo, 'commit', '-q', '-m', 'Documentation, tables, tools and REPRODUCE.md', env=env)
    return log, tags


def write_tables(repo: Path, built: list[dict]):
    out = []
    for b in built:
        act = b['act']
        first = b['versions'][0]
        out.append({'act': act['short'], 'enactment': act['id'], 'title': act['short'], 'in_force': first['from'],
                    'provisions': 'all', 'note': 'first version', 'source': first['pdf']})
        for r in b['table']:
            out.append({'act': act['short'], 'enactment': r['law'], 'title': b['laws'][r['law']]['title'], 'in_force': r['date'],
                        'provisions': r['provisions'], 'note': r.get('note') or '', 'source': b['laws'][r['law']]['url']})
    out.sort(key=lambda r: (r['in_force'], r['act'], r['enactment']))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(out[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(out)
    (repo / 'enactments.csv').write_text(buf.getvalue(), encoding='utf-8', newline='\n')
    for b in built:
        act = b['act']
        last = b['versions'][-1]
        counts: dict[str, int] = {}
        lastday: dict[str, str] = {}
        for ch in b['changes']:
            for ks in ch['groups'].values():
                for k in ks:
                    counts[k] = counts.get(k, 0) + 1
                    lastday[k] = ch['from']
        lines = [f'# {act["short"]}', '', f'<{b["page"]["url"]}>', '',
                 f'{len(b["versions"])} dated versions on the site, in force from {b["versions"][0]["from"]} (latest {last["from"]}).', '',
                 '| Provision | File | Changes | Last changed |', '| --- | --- | ---: | --- |']
        for k, u in last['units'].items():
            lines.append(f'| {u["label"]} | [{file_of(k)}]({file_of(k)}) | {counts.get(k, 0)} | {lastday.get(k, "")} |')
        (repo / act['slug'] / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')


def data_day() -> str:
    files = [p for p in CACHE.iterdir() if p.name != '.gitignore'] if CACHE.exists() else []
    if not files:
        return dt.date.today().isoformat()
    return dt.date.fromtimestamp(max(p.stat().st_mtime for p in files)).isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(ROOT.parent / 'gibraltar-law'))
    ap.add_argument('--offline', action='store_true')
    ap.add_argument('--today', default=None)
    ap.add_argument('--verify-rebuild', action='store_true')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if args.verify_rebuild:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = subprocess.run([sys.executable, '-X', 'utf8', str(HERE / 'build.py'), '--offline', '--repo', tmp]
                                 + (['--today', args.today] if args.today else []), capture_output=True, text=True, encoding='utf-8')
            if out.returncode:
                raise SystemExit(out.stderr)

            def hashes(r):
                log = git(Path(r), 'log', '--format=%H', 'main').split()
                tg = dict(l.split(' ', 1)[::-1] for l in git(Path(r), 'show-ref', '--tags').split('\n') if l)
                return log, tg
            a, b = hashes(args.repo), hashes(tmp)
            rec = {'identical': a[0][1:] == b[0][1:] and a[1] == b[1], 'history_tip': a[0][1], 'commits': len(a[0]) - 1,
                   'tags': len(a[1]), 'main_identical': a[0][0] == b[0][0], 'main': a[0][0], 'rebuilt_main': b[0][0]}
            print(json.dumps(rec, indent=1))
            p = HERE / 'verification.json'
            ver = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
            ver['rebuild'] = {k: rec[k] for k in ('identical', 'history_tip', 'commits', 'tags')}
            p.write_text(json.dumps(ver, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
            for f in Path(tmp).rglob('*'):
                os.chmod(f, 0o700)
            raise SystemExit(0 if rec['identical'] else 1)
    built = [build_act(a, args.offline) for a in ACTS]
    today = args.today or data_day()
    for b in built:
        n = sum(len(ks) for ch in b['changes'] for ks in ch['groups'].values())
        print(f'{b["act"]["slug"]}: {len(b["versions"])} versions {b["versions"][0]["from"]}..{b["versions"][-1]["from"]}, '
              f'{len(b["versions"][-1]["units"])} units, {n} unit changes')
        for p in b['problems']:
            print('   PROBLEM', p)
        for ch in b['changes']:
            print('  ', ch['from'], {g: len(k) for g, k in ch['groups'].items()}, sorted(set(ch['why'].values())))
    if os.environ.get('NO_WRITE'):
        return
    log, tags = write_repo(Path(args.repo), built, HERE / 'repo', today)
    print(f'repo: {len(log)} commits + 1 documentation commit, {len(tags)} tags -> {args.repo}')


if __name__ == '__main__':
    main()
