# How this history was made, and how to make it again

This file records how the repository was built: the sources, the commands, the software, the decisions made by hand,
and what an AI model did and did not do. The build writes it.

## Short version

```sh
git clone https://github.com/lexifina/gibraltar-law && cd gibraltar-law
pip install pymupdf
python -X utf8 tools/build.py --repo ../rebuilt --today 2026-10-28
git -C ../rebuilt rev-parse main        # the same hash as this repository's main
python -X utf8 tools/check_repo.py --repo ../rebuilt
python -X utf8 tools/test_repo.py --repo ../rebuilt
```

`tools/build.py` needs Python 3.12 or later, PyMuPDF and git. It reads the Gibraltar Laws site (or its own cache, `.cache/`
next to the script) and writes the repository into `--repo`. With the same site data and the same `--today` it gives the
same commits with the same hashes. `data/versions.json` lists every PDF read with its sha256.

## Sources

All legal text comes from the **Gibraltar Laws website** (www.gibraltarlaws.gov.gi, Government of Gibraltar), which
publishes every act in each dated version as a PDF. Nothing was typed in or rewritten. The build read 8 pages and
18 PDFs on 2026-10-28:

| Act | Folder | Versions | In force from | Files today |
| --- | --- | ---: | --- | ---: |
| Gibraltar Constitution Order 2006 | `constitution/` | 1 | 2007-01-02 to 2007-01-02 | 98 |
| Stamp Duties Act 2005 | `stamp-duties/` | 11 | 2006-01-12 to 2024-12-23 | 60 |

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
   this repository (git blob of `build.py`: `40d4127a4a2dfd5660d5e64744a1e70d692c7bdc`; `tools/` here holds the same files). Later builds ran with
   `--offline`, from the cache.
2. `check_repo.py` read every version of each act back from this repository with `tools/on_date.py` and compared it with
   the PDF, parsed afresh: file by file, and word for word against PyMuPDF's own word list for the PDF (read without
   the parser). Result: 12 versions checked (718 files), 0 mismatches; 12 versions word for word (144770 words), 0 mismatches.
3. `test_repo.py --record` ran the functional smoke test:
   - pass: blame names an enactment: stamp-duties/sch-1.md lines by Act 2005-73, Act 2010-17, Act 2014-02, Act 2019-25, Act 2023-17, Act 2024-37
   - pass: text before and after an amendment: stamp-duties/s-019B.md 2018-06-30 != 2018-07-01; stamp-duties/sch-1.md 2015-12-31 != 2016-01-01
   - pass: log --follow in date order: stamp-duties/sch-1.md 11 commits; stamp-duties/s-002.md 3 commits
   - pass: tags resolve, In-force on every law commit, trailers parse: 24 tags resolve; 12 law commits carry In-force and parse
   - pass: only the documentation commit is by Lexifina: only the documentation commit 4bf3469024 is by Lexifina; 8 distinct authors
   - pass: corpus.json matches the history: history_from 2006-01-12, record_to 2024-12-23
   - pass: README commands run: 10 README commands ran
4. `build.py --offline --verify-rebuild` built the repository again from the same cache into a temporary folder and
   compared hashes. The last law commit was `ad3d4b46897bc4233e16a6d54877b24973b80ca8` in both builds, and all 12 law commits and 24 tags had the same hash.
5. `git push -f origin main --tags` published the first final build to the private repository `lexifina/gibraltar-law`.
   Later changes are appended, never forced.

It ran with Python 3.12.10, PyMuPDF 2.0 and git version 2.46.0.windows.1 on Windows 11.

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
     section that contains it), otherwise "date only" (2
     file changes), recorded in the `Evidence:` trailer;
  2. several enactments: the one whose listed provisions name the file; if that is not exactly one, the change is
     credited to none, committed by the publisher and labelled with `Candidate:` trailers (0 commits this build);
  3. no enactment: committed by the publisher, labelled (0 commits this build).
  The title page, long title and arrangement of sections follow whichever enactment changed provisions that day.
- **Commits.** 2 commits for the first version of each act, 10 law commits (0 change no file),
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
  `order/2006-constitution` for the first versions; 24 in all.
- **Documentation commit.** Dated 2026-10-28, the day the data was retrieved, so a rebuild of the same data on a later day gives
  the same hash.

Changes credited by date only (the provision is not named in the table row):

- 2018-07-01: s-024
- 2018-07-01: s-025

Problems the build found in the source (empty means none):

- none

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

Built on 2026-10-28 in **Claude Code** by the model **Claude Sonnet 5.5** (`claude-sonnet-5-5`), working from a brief by the
user at Lexifina. The model researched the source, wrote all the code here (`tools/build.py`, `reproduce.py`,
`check_repo.py`, `test_repo.py`, `on_date.py`), the README, the licence note and this file, ran the commands above and
checked the results. It did **not** write or edit any legal text: every word, date and title is copied by the script from
the site. No model runs when the history is built or checked. A lawyer has not reviewed the work line by line.
