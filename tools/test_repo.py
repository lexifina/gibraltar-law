"""Functional smoke test of the built Gibraltar law repository: the things a reader does with it work. Standard library only.

    python -X utf8 scripts/gibraltar-law/test_repo.py [--repo ../gibraltar-law] [--record]
    python -X utf8 tools/test_repo.py                   # from inside the repository

It asserts that:
1. `git blame` on a changed provision names an amending enactment as author of its lines;
2. tools/on_date.py gives the text before and after a known amendment, and each equals the file at that day's commit;
3. `git log --follow` on a file lists its enactments in the order they took effect;
4. every tag resolves to a commit, every commit but the documentation commit has an `In-force:` trailer, and every
   commit's trailers parse with `git interpret-trailers --parse`;
5. no commit is authored by Lexifina except the documentation commit (the last one), and every author address is `.invalid`;
6. every git or tool command in the README's table runs and prints something;
7. corpus.json carries history_from, record_to and in_force_trailer, equal to the history.
With --record the result is written to verification.json next to this script (for REPRODUCE.md).
"""
import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAW = re.compile(r'^(Act \d{4}-\d+|Gibraltar Constitution Order 2006)$')
PUBLISHER = 'Gibraltar Law Offices (gibraltarlaws.gov.gi)'


def default_repo() -> Path:
    if (HERE.parent / '.git').exists():
        return HERE.parent
    return HERE.parents[2] / 'gibraltar-law'


class Smoke:
    def __init__(self, repo: Path):
        self.repo = repo
        self.results: list[tuple[str, bool, str]] = []

    def git(self, *args: str) -> str:
        out = subprocess.run(['git', *args], cwd=self.repo, capture_output=True, text=True, encoding='utf-8')
        if out.returncode:
            raise AssertionError(f'git {" ".join(args)}: {out.stderr.strip()}')
        return out.stdout

    def tool(self, *args: str) -> str:
        out = subprocess.run([sys.executable, '-X', 'utf8', 'tools/on_date.py', *args], cwd=self.repo, capture_output=True,
                             text=True, encoding='utf-8')
        if out.returncode:
            raise AssertionError(f'on_date {" ".join(args)}: {out.stderr.strip()}')
        return out.stdout

    def check(self, name: str, fn):
        try:
            detail = fn() or ''
            self.results.append((name, True, detail))
            print(f'PASS {name}: {detail}')
        except AssertionError as exc:
            self.results.append((name, False, str(exc)))
            print(f'FAIL {name}: {exc}')

    def blame(self):
        out = self.git('blame', '--line-porcelain', 'main', '--', 'stamp-duties/sch-1.md')
        authors = {l[7:] for l in out.splitlines() if l.startswith('author ')}
        assert authors and all(LAW.match(a) or a == PUBLISHER for a in authors), f'unexpected authors {authors}'
        assert 'Act 2019-25' in authors and len(authors) >= 3, f'authors {authors}'
        return f'stamp-duties/sch-1.md lines by {", ".join(sorted(authors))}'

    def on_date(self):
        done = []
        for path, prov, tag, before, after in [
                ('stamp-duties/s-019B.md', '19B', 'act/2019-25/2018-07-01', '2018-06-30', '2018-07-01'),
                ('stamp-duties/sch-1.md', 'sch-1', 'act/2023-17/2016-01-01', '2015-12-31', '2016-01-01')]:
            a, b = self.tool(before, 'stamp-duties', prov) if prov != '19B' else '', self.tool(after, 'stamp-duties', prov)
            if prov == '19B':
                try:
                    self.tool(before, 'stamp-duties', prov)
                    raise AssertionError('s. 19B exists before it was inserted')
                except AssertionError as exc:
                    assert 'not in the text' in str(exc), exc
                a = None
            else:
                assert a and b and a != b, f'{path}: no change between {before} and {after}'
                assert a == self.git('show', f'{tag}~1:{path}'), f'{path} on {before} is not the file before {tag}'
            assert b == self.git('show', f'{tag}:{path}'), f'{path} on {after} is not the file at {tag}'
            done.append(f'{path} {before} != {after}')
        whole = self.tool('2020-01-01', 'stamp-duties')
        assert 'Special Stamp Duty' in whole, 'whole act on 2020-01-01 lacks s. 19B'
        c = self.tool('2020-01-01', 'constitution', 'annex1/8')
        assert 'No person shall be held to be guilty of a criminal offence' in c, 'Constitution s. 8 missing'
        return '; '.join(done)

    def follow(self):
        checked = []
        for path in ('stamp-duties/sch-1.md', 'stamp-duties/s-002.md'):
            out = self.git('log', '--follow', '--format=%an%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', path)
            rows = [l.split('\t') for l in out.splitlines() if l]
            days = [d.strip() for _, d in rows]
            assert len(rows) >= 2, f'{path}: {len(rows)} commits'
            assert days == sorted(days, reverse=True), f'{path}: not in date order {days}'
            assert all(LAW.match(a) or a == PUBLISHER for a, _ in rows), f'{path}: authors {[a for a, _ in rows]}'
            checked.append(f'{path} {len(rows)} commits')
        return '; '.join(checked)

    def tags_and_trailers(self):
        tags = self.git('tag').split()
        assert tags, 'no tags'
        for t in tags:
            self.git('rev-parse', '--verify', '-q', f'{t}^{{commit}}')
        rows = self.git('log', '--format=%H%x09%an%x09%(trailers:key=In-force,valueonly,separator=)', 'main').splitlines()
        missing = [r for r in rows[1:] if not r.split('\t')[2].strip()]
        assert not missing, f'{len(missing)} commits without In-force'
        assert not rows[0].split('\t')[2].strip(), 'documentation commit should carry no In-force'
        bad = [r for r in rows[1:] if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', r.split('\t')[2].strip())]
        assert not bad, f'malformed In-force {bad[:2]}'
        unparsed = 0
        for r in rows[1:]:
            body = self.git('log', '-1', '--format=%B', r.split('\t')[0])
            out = subprocess.run(['git', 'interpret-trailers', '--parse'], input=body, cwd=self.repo, capture_output=True,
                                 text=True, encoding='utf-8').stdout
            if 'In-force:' not in out:
                unparsed += 1
        assert not unparsed, f'{unparsed} commits whose trailers do not parse'
        return f'{len(tags)} tags resolve; {len(rows) - 1} law commits carry In-force and parse'

    def lexifina(self):
        rows = self.git('log', '--format=%H%x09%an%x09%ae%x09%cn', 'main').splitlines()
        by_lex = [r for r in rows if r.split('\t')[1] == 'Lexifina']
        assert len(by_lex) == 1 and by_lex[0] == rows[0], f'{len(by_lex)} commits by Lexifina'
        assert all(r.split('\t')[3] == 'Lexifina' for r in rows), 'a committer other than Lexifina'
        assert all(r.split('\t')[2].endswith('.invalid') for r in rows[1:]), 'an author address that is not .invalid'
        authors = {r.split('\t')[1] for r in rows[1:]}
        assert all(LAW.match(a) or a == PUBLISHER for a in authors), f'unexpected authors {authors}'
        return f'only the documentation commit {rows[0][:10]} is by Lexifina; {len(authors)} distinct authors'

    def corpus(self):
        c = json.loads((self.repo / 'corpus.json').read_text(encoding='utf-8'))
        days = sorted(set(re.findall(r'^In-force: (\S+)', self.git('log', '--format=%B', 'main'), re.M)))
        assert c['in_force_trailer'] == 'In-force'
        assert c['history_from'] == days[0] and c['record_to'] == days[-1], (c['history_from'], c['record_to'], days[0], days[-1])
        assert c['scope']['default_reach']['decided_here'] is False
        return f'history_from {c["history_from"]}, record_to {c["record_to"]}'

    def readme(self):
        text = (self.repo / 'README.md').read_text(encoding='utf-8')
        table = text[text.index('## The questions'):text.index('Raw git, by')]
        cmds = [c for c in re.findall(r'`([^`]+)`', table) if c.startswith(('git ', 'python '))]
        assert len(cmds) >= 8, f'only {len(cmds)} commands found'
        for c in cmds:
            args = shlex.split(c)
            if args[0] == 'python':
                args[:1] = [sys.executable, '-X', 'utf8']
            out = subprocess.run(args, cwd=self.repo, capture_output=True, text=True, encoding='utf-8')
            assert out.returncode == 0, f'{c}: exit {out.returncode} {out.stderr.strip()[:200]}'
            if 'Candidate:' not in c:   # no day with two enactments occurs in the current texts
                assert out.stdout.strip(), f'{c}: printed nothing'
        return f'{len(cmds)} README commands ran'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=None)
    ap.add_argument('--record', action='store_true')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    s = Smoke(Path(args.repo) if args.repo else default_repo())
    s.check('blame names an enactment', s.blame)
    s.check('text before and after an amendment', s.on_date)
    s.check('log --follow in date order', s.follow)
    s.check('tags resolve, In-force on every law commit, trailers parse', s.tags_and_trailers)
    s.check('only the documentation commit is by Lexifina', s.lexifina)
    s.check('corpus.json matches the history', s.corpus)
    s.check('README commands run', s.readme)
    ok = all(r[1] for r in s.results)
    print(f'{sum(r[1] for r in s.results)}/{len(s.results)} passed')
    if args.record:
        p = HERE / 'verification.json'
        rec = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        rec['smoke'] = {'passed': sum(r[1] for r in s.results), 'total': len(s.results),
                        'results': [{'test': n, 'ok': o, 'detail': d} for n, o, d in s.results]}
        p.write_text(json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
