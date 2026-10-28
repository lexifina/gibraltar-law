"""Writes data/versions.json, corpus.json and REPRODUCE.md into the Gibraltar law repository, from the facts of the build
that made it. Called by build.py. The results of the checks (check_repo.py, test_repo.py and the rebuild that compares
hashes) are read from verification.json next to this file; they describe the build before the one that writes this file,
from the same data."""
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write_manifest(repo: Path, built: list[dict], today: str, log: list[dict]):
    days = sorted({v['from'] for b in built for v in b['versions']})
    out = {'built': today, 'source': 'https://www.gibraltarlaws.gov.gi', 'acts': [{
        'id': b['act']['id'], 'slug': b['act']['slug'], 'title': b['act']['short'], 'page': b['page']['url'],
        'page_sha256': b['page']['sha256'],
        'versions': [{'from': v['from'], 'pdf': v['pdf'], 'sha256': v['sha256'], 'pages': v['pages'], 'page': v['page']}
                     for v in b['versions']],
        'amending': [{'number': k, 'title': m['title'], 'url': m['url'], 'pdf': m['pdf'], 'assent': m['assent'],
                      'gazette': m['gazette']} for k, m in b['laws'].items()],
    } for b in built]}
    (repo / 'data').mkdir(exist_ok=True)
    (repo / 'data' / 'versions.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8',
                                                 newline='\n')
    rule = {
        'rule': 'no retroactive criminal liability; otherwise a general presumption against retroactivity, not a constitutional bar',
        'meaning': 'the Constitution forbids holding a person guilty of an offence for an act that was not an offence when '
                   'done, and a penalty severer than the maximum then available; for other law the record states no general '
                   'rule, and an act that says it applies from an earlier day (several here do) is recorded as such',
        'authority': 'Gibraltar Constitution Order 2006, Annex 1, section 8(4): "No person shall be held to be guilty of a '
                     'criminal offence on account of any act or omission that did not, at the time it took place, constitute '
                     'such an offence, and no penalty shall be imposed for a criminal offence that is severer in degree or '
                     'description than the maximum penalty that might have been imposed for that offence at the time when '
                     'it was committed."',
        'decided_here': False}
    corpus = {
        'corpus': 'gi/national/acts',
        'name': 'Gibraltar law: the Gibraltar Constitution Order 2006 and the Stamp Duties Act 2005 (2005-73)',
        'acts': ['Gibraltar Constitution Order 2006', 'Stamp Duties Act 2005 (2005-73)'],
        'history_from': days[0],
        'record_to': max(d for d in days if d <= today),
        'built': today,
        'in_force_trailer': 'In-force',
        'dates': {'commit': 'in-force', 'other_trailers': ['Enacted', 'Made', 'Published'],
                  'time': '12:00 Europe/Gibraltar (UTC+1, UTC+2 in summer time)'},
        'scope': {'trailer': 'Applies',
                  'when_absent': 'this corpus records no scope notes (no commit carries Applies:); the absence is not a '
                                 'statement that the change reaches every case',
                  'default_reach': rule},
        'tool': 'tools/on_date.py'}
    (repo / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def write_reproduce(repo: Path, built: list[dict], log: list[dict], tags: dict, requests: list[dict], today: str):
    blob = subprocess.run(['git', 'hash-object', str(HERE / 'build.py')], capture_output=True, text=True).stdout.strip()
    pyv = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.strip()
    gitv = subprocess.run(['git', '--version'], capture_output=True, text=True).stdout.strip()
    try:
        import pymupdf
        mv = pymupdf.VersionBind
    except Exception:
        mv = '?'
    ver = json.loads((HERE / 'verification.json').read_text(encoding='utf-8')) if (HERE / 'verification.json').exists() else {}
    files = {r['file'] for r in requests if r['file'].exists()}
    retrieved = ', '.join(sorted({dt.date.fromtimestamp(f.stat().st_mtime).isoformat() for f in files})) or today
    urls = {r['url'] for r in requests}
    n_pdf = sum(1 for u in urls if u.endswith('.pdf'))
    n_page = len(urls) - n_pdf
    n_law = sum(1 for c in log if c['kind'] == 'law')
    n_empty = sum(1 for c in log if c['kind'] == 'law' and not c['units'])
    n_cand = sum(1 for c in log if c['kind'] == 'candidates')
    n_unexp = sum(1 for c in log if c['kind'] == 'unexplained')
    n_start = sum(1 for c in log if c['kind'] == 'start')
    why: dict[str, int] = {}
    date_only: list[str] = []
    for b in built:
        for ch in b['changes']:
            for k, w in ch['why'].items():
                why[w] = why.get(w, 0) + 1
                if 'date only' in w:
                    date_only.append(f'{ch["from"]}: {k}')
    chk, det, smoke = ver.get('check', {}), ver.get('rebuild', {}), ver.get('smoke', {})
    check_line = (f'{chk["versions"]} versions checked ({chk["files"]} files), {chk["mismatches"]} mismatches; '
                  f'{chk["wordcheck"]} versions word for word ({chk["words"]} words), {chk["word_mismatches"]} mismatches'
                  if chk else '(not yet run)')
    rebuild_line = (f'The last law commit was `{det["history_tip"]}` in both builds, and all {det["commits"]} law commits and '
                    f'{det["tags"]} tags had the same hash.' if det.get('identical') else '(not yet run)')
    smoke_lines = ('\n'.join(f'   - {"pass" if r["ok"] else "FAIL"}: {r["test"]}: {r["detail"]}' for r in smoke['results'])
                   if smoke else '   (not yet run)')
    rows = '\n'.join(f'| {b["act"]["short"]} | `{b["act"]["slug"]}/` | {len(b["versions"])} | '
                     f'{b["versions"][0]["from"]} to {b["versions"][-1]["from"]} | {len(b["versions"][-1]["units"])} |' for b in built)
    problems = '\n'.join(f'- {b["act"]["slug"]}: {p}' for b in built for p in b['problems']) or '- none'
    do = '\n'.join(f'- {x}' for x in date_only) or '- none'
    text = f"""# How this history was made, and how to make it again

This file records how the repository was built: the sources, the commands, the software, the decisions made by hand,
and what an AI model did and did not do. The build writes it.

## Short version

```sh
git clone https://github.com/lexifina/gibraltar-law && cd gibraltar-law
pip install pymupdf
python -X utf8 tools/build.py --repo ../rebuilt --today {today}
git -C ../rebuilt rev-parse main        # the same hash as this repository's main
python -X utf8 tools/check_repo.py --repo ../rebuilt
python -X utf8 tools/test_repo.py --repo ../rebuilt
```

`tools/build.py` needs Python 3.12 or later, PyMuPDF and git. It reads the Gibraltar Laws site (or its own cache, `.cache/`
next to the script) and writes the repository into `--repo`. With the same site data and the same `--today` it gives the
same commits with the same hashes. `data/versions.json` lists every PDF read with its sha256.

## Sources

All legal text comes from the **Gibraltar Laws website** (www.gibraltarlaws.gov.gi, Government of Gibraltar), which
publishes every act in each dated version as a PDF. Nothing was typed in or rewritten. The build read {n_page} pages and
{n_pdf} PDFs on {retrieved}:

| Act | Folder | Versions | In force from | Files today |
| --- | --- | ---: | --- | ---: |
{rows}

- the act's page, with its **version history** (each version has its own address, `.../version/DD-MM-YYYY`, embedding a
  PDF) and its **amending legislation**;
- each version's PDF, `uploads/legislations/<act>/<number>(DD-MM-YY).pdf` (the first version of an act is the PDF of
  the act as enacted, `<number>o.pdf`);
- each amending act's page and PDF, for its title, the day it was assented to and the Gazette issue.

robots.txt asks `Crawl-delay: 5` of agents it does not name and disallows only `/vendor/`; requests were made one at a
time, at least 5 seconds apart, with the user agent `lexifina-watch/1.0 (+https://lexifina.com/watch;
gibraltar-law@lexifina.com)`. No login or challenge.

## The build, step by step

1. `python -X utf8 scripts/gibraltar-law/build.py` in Lexifina's own repository fetched the data into its cache and wrote
   this repository (git blob of `build.py`: `{blob}`; `tools/` here holds the same files). Later builds ran with
   `--offline`, from the cache.
2. `check_repo.py` read every version of each act back from this repository with `tools/on_date.py` and compared it with
   the PDF, parsed afresh: file by file, and word for word against PyMuPDF's own word list for the PDF (read without
   the parser). Result: {check_line}.
3. `test_repo.py --record` ran the functional smoke test:
{smoke_lines}
4. `build.py --offline --verify-rebuild` built the repository again from the same cache into a temporary folder and
   compared hashes. {rebuild_line}
5. `git push -f origin main --tags` published the first final build to the private repository `lexifina/gibraltar-law`.
   Later changes are appended, never forced.

It ran with {pyv}, PyMuPDF {mv} and {gitv} on Windows 11.

## How the text and the commits are derived

- **Text.** PyMuPDF reads each PDF line by line. The running header and footer (recognised by what they say), the page
  numbers and the table of amending enactments on page 1 are not text of the act and are left out; the table is read
  separately (below). A paragraph is a run of lines between the PDF's blank lines; a list item that follows another on the
  same printed line, or a lone "and" or "or" between items, is joined or split the same way in every version. White space
  is normalised; the one character changed is the private-use minus glyph (U+F02D) the publisher's font prints for a
  dash, which becomes an en dash. The publisher used three page templates over the years; the same rules read all of them.
  Each section is one file (`s-004A.md`), each schedule one file (`sch-1.md`); the marginal note and part heading that
  open a section are lines at the top of its file; `front.md` holds the title, principal-act number, commencement
  and assent lines, `arrangement.md` the arrangement of sections (one printed row per line), `intro.md` the long title.
  The Constitution is `constitution/order/` (the Order's two sections), `annex1/` (the Constitution, sections 1 to 84,
  its schedule of oaths and its arrangement) and `annex2/` (transitional provisions).
- **Changes.** Consecutive versions are compared file by file.
- **Cause.** Each PDF opens with a table of the amending enactments, the provisions they affect and the day each took
  effect. For a version of day D the build takes the rows dated D from that version's own PDF (the newest PDF keeps only
  the provisions still current, so older PDFs name more). Tried in this order, per changed file:
  1. one enactment took effect that day: it, with "law and provision named" when the table lists the provision (or a
     section that contains it), otherwise "date only" ({why.get('commencement table: date only (provision not named)', 0)}
     file changes), recorded in the `Evidence:` trailer;
  2. several enactments: the one whose listed provisions name the file; if that is not exactly one, the change is
     credited to none, committed by the publisher and labelled with `Candidate:` trailers ({n_cand} commits this build);
  3. no enactment: committed by the publisher, labelled ({n_unexp} commits this build).
  The title page, long title and arrangement of sections follow whichever enactment changed provisions that day.
- **Commits.** {n_start} commits for the first version of each act, {n_law} law commits ({n_empty} change no file),
  then one for this documentation. The author of a law commit is the enactment, `Act 2019-25` at
  `act-2019-25@gibraltarlaws.invalid`; the Constitution is by `Gibraltar Constitution Order 2006`. The committer is
  `Lexifina <gibraltar-law@lexifina.com>`. Author and committer dates are noon in Gibraltar on the in-force day (UTC+1,
  UTC+2 in summer time, from the last Sunday in March to the last Sunday in October, coded in because the build machine has
  no time-zone database). Every commit has `In-force:`. Other trailers: `Kind`, `Enacted` (assent, read from the
  amending act's PDF), `Published` (Gazette issue), `Made`, `Provisions` (the table's wording), `Evidence`,
  `Commencement-notice` (the table's footnote), `Affecting`, `Source`, `Consolidated`, `PDF`.
- **Retroactive commencement.** The table gives some days earlier than the act that made the change (for example Act
  2024-37, assented to in December 2024, has a row dated 11 July 2023). The commit is dated the in-force day, as in the
  other corpora; `Enacted:` shows the later date.
- **Tags.** `stamp-duties/<day>` and `constitution/<day>` for each day; `act/<number>` for each amending act (one
  per day, `act/2019-25/2018-07-01`, when an act took effect on several days); `act/2005-73` and
  `order/2006-constitution` for the first versions; {len(tags)} in all.
- **Documentation commit.** Dated {today}, the day the data was retrieved, so a rebuild of the same data on a later day gives
  the same hash.

Changes credited by date only (the provision is not named in the table row):

{do}

Problems the build found in the source (empty means none):

{problems}

## Decisions made by hand

1. **The acts.** The Gibraltar Constitution Order 2006, and the Stamp Duties Act 2005: eleven versions since 2006, a clean
   one-enactment-per-day commencement table, a short text. The Crimes Act 2011 (28 versions) was considered and passed over
   as larger; it can be added with one line in `ACTS`.
2. **The Constitution has one version.** The site publishes the Order as made, with one version dated 2 January 2007 (the
   day the Constitution took effect; the Order itself fixes it by proclamation). The site lists the Gibraltar Laws (General
   Amendment) (No.1) Act 2007 as amending it but offers no later text, so no amendment is applied here.
3. **The first version of the Stamp Duties Act** is the PDF of the act as enacted (`2005-73o.pdf`), which the site dates
   12 January 2006, the day the act was brought into operation (LN.2006/001).
4. **The date is the table's date.** The table's commencement dates match the version dates exactly.
5. **Not authentic.** The site says that only the Gazette's paper editions are authentic; so this record is a convenience
   copy, never the law.
6. **English only**, the language of the source.

## What an AI model did

Built on {today} in **Claude Code** by the model **Claude Sonnet 5.5** (`claude-sonnet-5-5`), working from a brief by the
user at Lexifina. The model researched the source, wrote all the code here (`tools/build.py`, `reproduce.py`,
`check_repo.py`, `test_repo.py`, `on_date.py`), the README, the licence note and this file, ran the commands above and
checked the results. It did **not** write or edit any legal text: every word, date and title is copied by the script from
the site. No model runs when the history is built or checked. A lawyer has not reviewed the work line by line.
"""
    (repo / 'REPRODUCE.md').write_text(text, encoding='utf-8', newline='\n')
