# Gibraltar law, change by change

Two texts of Gibraltar as a git repository: the Gibraltar Constitution Order 2006 and the Stamp Duties Act 2005
(Act 2005-73). Each amending enactment is one commit, credited to that enactment and dated the day it took effect, at
noon in Gibraltar. The text is read from the PDFs on the Government of Gibraltar's
[Gibraltar Laws](https://www.gibraltarlaws.gov.gi) site. **This is a private working copy: the site says only the
Gazette's paper editions are authentic, and its reuse terms are unclear (see `LICENSE`).**

## The questions, as git commands

| Question | Command |
| --- | --- |
| What did section 19B say on 1 January 2019? | `python tools/on_date.py 2019-01-01 stamp-duties 19B` |
| The whole Stamp Duties Act as it stood in 2012 | `python tools/on_date.py 2012-01-01 stamp-duties` |
| Schedule 1 on 1 January 2022 | `python tools/on_date.py 2022-01-01 stamp-duties sch-1` |
| Section 8 of the Constitution (protection of law) | `python tools/on_date.py 2020-01-01 constitution annex1/8` |
| Which enactment wrote each line of Schedule 1? | `git blame stamp-duties/sch-1.md` |
| Every change to Schedule 1, with the enactment and the day | `git log --follow stamp-duties/sch-1.md` |
| Everything one enactment changed on one day | `git show --stat act/2019-25/2018-07-01` |
| What changed in the act on one day | `git show --stat stamp-duties/2023-08-01` |
| The enactments with their dates | [`enactments.csv`](enactments.csv) |
| Changes credited by date only | `git log --grep="date only" --format="%an %s"` |
| Changes the table could not separate between two enactments | `git log --grep="Candidate:" --format="%an %s"` |

Raw git, by the `In-force` day (bash): `git show "$(git rev-list -1 --before=2019-01-01T23:59:59Z main -- stamp-duties):stamp-duties/s-019B.md"`.
PowerShell: `$r = git rev-list -1 --before=2019-01-01T23:59:59Z main -- stamp-duties; git show "$($r):stamp-duties/s-019B.md"`.
The `on_date.py` tool reads the `In-force` trailer, which is exact; commit times are only noon. After a rebuild, use
`git fetch --force --tags` to replace stale tags.

## The dates, and which one we use

An act has the day it was assented to (`Enacted:`), the Gazette issue (`Published:`) and the day it took effect
(`In-force:`). **Commits are dated the day the change took effect**, at noon in Gibraltar (CET, CEST in summer). Some
in-force days are earlier than the enactment (Act 2024-37, assented to in December 2024, has a row dated 11 July 2023):
the commit keeps the in-force day and `Enacted:` shows the later one. The Constitution is dated 2 January 2007, the day
the site gives for its one version.

## What "author" means

The author of a commit is the amending enactment, `Act 2019-25` at `act-2019-25@gibraltarlaws.invalid` (an address that
cannot exist), so `git blame` names the enactment. Every PDF opens with a table of the amending enactments, the provisions
each affects and the day it took effect; that day is the version's day. A change is credited to the enactment the table
gives for that day: with the provision named, or "date only" when the table does not list the provision (the `Evidence:`
trailer says which). Where several enactments took effect the same day and their provisions cannot separate the change,
it is committed by `Gibraltar Law Offices (gibraltarlaws.gov.gi)`, labelled, with `Candidate:` trailers, and credited to
none (no such day occurs in these two texts). A change no row explains is committed by the publisher and labelled. The
committer is always `Lexifina`.

## How it is checked

`tools/check_repo.py` reads every version back from git on the day it took effect and compares it, file by file, with the
text parsed afresh from the PDF, and word for word with PyMuPDF's own word list for the PDF. `tools/test_repo.py` checks the
commands above. The results, and the exact commands to rebuild this repository hash for hash, are in
[`REPRODUCE.md`](REPRODUCE.md).

## Files

`stamp-duties/s-004A.md` is section 4A, `stamp-duties/sch-1.md` Schedule 1, `front.md` the title page, `arrangement.md` the
arrangement of sections, `intro.md` the long title. `constitution/annex1/s-008.md` is section 8 of the Constitution;
`constitution/order/` holds the Order's own two sections and `constitution/annex2/` the transitional provisions. The
marginal note and part heading open each section's file. One paragraph per line, separated by a blank line.

## What it does not show

- The PDFs are the only source of text. Layout (columns, indentation) is lost; schedule tables read in the PDF's own order.
- The Constitution has **one** version on the site (as made, in force 2 January 2007). Later amendments (for example by the
  Gibraltar Laws (General Amendment) (No.1) Act 2007) are not applied.
- The first version of the Stamp Duties Act is the act as enacted; the site dates it 12 January 2006.
- The Gazette, not this repository, is authentic. Reuse terms of the source are unclear.
- Blame credits whole lines: one changed word credits the whole paragraph.
- Words the publisher changed without any amendment (for example hyphen repairs) appear under the enactment of that
  day, marked "date only".

## Built how

`tools/build.py` (Python 3.12, PyMuPDF, git). The same data gives the same hashes.
