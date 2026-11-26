# Structure

```
constitution/                       Gibraltar Constitution Order 2006 (order/, annex1/ = the Constitution, annex2/)
acts/<year>/<number>-<name>/        Acts of Parliament, by year and number (acts/2011/023-crimes-act/ = Act 2011-23)
subsidiary/<year>/<number>-<name>/  Subsidiary legislation, by Legal Notice year and number (subsidiary/2021/329-abortion-regulations/)
```

Inside each instrument folder: one file per section or regulation (`s-001.md`, `s-004A.md`), one per schedule
(`sch-1.md`), and `front.md` for the title page, the publisher's table of amending enactments and the arrangement.
A PDF with no numbered sections is kept whole as `text.md`. No folder holds more than 1,000 entries.

Commits: one per dated consolidated version on gibraltarlaws.gov.gi, at noon Europe/Gibraltar on the day the version
took effect (the version day the site gives). The first commit of an instrument is credited to the instrument itself
and is the earliest version the site holds; each later one is credited to the amending enactments whose commencement
days, in the table that opens that version's PDF, fall since the previous version (`Act 2023-17`, `LN 2013/189`), or to
"Government of Gibraltar (consolidated version)" when the table names none. Trailers: `In-force:`, `Source:` (the
PDF), `Source-sha256:`, `Page:`, `Amended-by:`.

Corpus id: `gi/national/acts`. Case law: the separate repository gibraltar-law-caselaw.
